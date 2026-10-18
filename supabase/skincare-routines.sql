-- Apply to the existing GLOWME Supabase project. No storage bucket is required:
-- images are compressed raster data URLs inside the bounded steps JSON.
begin;
create or replace function public.valid_routine_steps(items jsonb)
returns boolean language plpgsql immutable set search_path = pg_catalog as $$
declare item jsonb; photo text;
begin
 if jsonb_typeof(items) <> 'array' or jsonb_array_length(items) not between 1 and 6 or octet_length(items::text)>1150000 then return false; end if;
 for item in select value from jsonb_array_elements(items) loop
  if jsonb_typeof(item)<>'object' or coalesce(length(btrim(item->>'title')),0) not between 1 and 60 or coalesce(length(btrim(item->>'body')),0) not between 1 and 600 then return false; end if;
  photo:=coalesce(item->>'image','');
  if length(photo)>180000 or (photo<>'' and photo !~ '^data:image/(jpeg|png|webp);base64,[A-Za-z0-9+/=]+$') then return false; end if;
 end loop;
 return true;
exception when others then return false;
end $$;
create table if not exists public.routine_posts (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references auth.users(id) on delete cascade,
 title text not null check(length(btrim(title)) between 1 and 100),
 body text not null default '' check(length(body)<=1000),
 period text not null check(period in ('am','pm')),
 skin text not null check(skin in ('건성','지성','복합성','중성','모든 피부')),
 steps jsonb not null check(public.valid_routine_steps(steps)),
 created_at timestamptz not null default now()
);
alter table public.routine_posts enable row level security;
drop policy if exists "public routine read" on public.routine_posts;
create policy "public routine read" on public.routine_posts for select to anon,authenticated using(true);
drop policy if exists "publish own routine" on public.routine_posts;
create policy "publish own routine" on public.routine_posts for insert to authenticated with check(user_id=auth.uid());
drop policy if exists "remove own routine" on public.routine_posts;
create policy "remove own routine" on public.routine_posts for delete to authenticated using(user_id=auth.uid());
grant select on public.routine_posts to anon,authenticated;
grant insert,delete on public.routine_posts to authenticated;
create index if not exists routine_posts_created_at_idx on public.routine_posts(created_at desc);
commit;
