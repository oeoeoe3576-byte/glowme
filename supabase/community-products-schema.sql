-- GLOWME community and product moderation schema (migration proposal)
-- NOT APPLIED: run in Supabase SQL editor after review.
create table if not exists public.products (
 id uuid primary key default gen_random_uuid(),
 brand text not null,
 name text not null,
 category text not null,
 image_url text,
 status text not null default 'pending' check(status in ('pending','approved','rejected')),
 submitted_by uuid references auth.users(id),
 reviewed_by uuid references auth.users(id),
 created_at timestamptz not null default now()
);
create table if not exists public.community_posts (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references auth.users(id),
 category text not null,
 title text not null,
 body text not null,
 product_id uuid references public.products(id),
 image_url text,
 created_at timestamptz not null default now()
);
create table if not exists public.community_comments (
 id uuid primary key default gen_random_uuid(),
 post_id uuid not null references public.community_posts(id) on delete cascade,
 user_id uuid not null references auth.users(id),
 body text not null,
 created_at timestamptz not null default now()
);
create table if not exists public.community_likes (
 post_id uuid not null references public.community_posts(id) on delete cascade,
 user_id uuid not null references auth.users(id),
 created_at timestamptz not null default now(),
 primary key(post_id,user_id)
);
create table if not exists public.admin_users (
 user_id uuid primary key references auth.users(id)
);
alter table public.products enable row level security;
alter table public.community_posts enable row level security;
alter table public.community_comments enable row level security;
alter table public.community_likes enable row level security;
alter table public.admin_users enable row level security;
-- Avoid exposing admin membership except to its owner.
create policy "own admin status" on public.admin_users for select to authenticated using(user_id=auth.uid());
create policy "products public approved or own" on public.products for select to authenticated using(status='approved' or submitted_by=auth.uid() or exists(select 1 from public.admin_users a where a.user_id=auth.uid()));
create policy "submit products" on public.products for insert to authenticated with check(submitted_by=auth.uid() and status='pending' and reviewed_by is null);
create policy "admin reviews products" on public.products for update to authenticated using(exists(select 1 from public.admin_users a where a.user_id=auth.uid())) with check(exists(select 1 from public.admin_users a where a.user_id=auth.uid()));
create policy "read posts" on public.community_posts for select to authenticated using(true);
create policy "create own posts" on public.community_posts for insert to authenticated with check(user_id=auth.uid());
create policy "delete own posts" on public.community_posts for delete to authenticated using(user_id=auth.uid());
create policy "read comments" on public.community_comments for select to authenticated using(true);
create policy "create own comments" on public.community_comments for insert to authenticated with check(user_id=auth.uid());
create policy "delete own comments" on public.community_comments for delete to authenticated using(user_id=auth.uid());
create policy "read likes" on public.community_likes for select to authenticated using(true);
create policy "create own likes" on public.community_likes for insert to authenticated with check(user_id=auth.uid());
create policy "remove own likes" on public.community_likes for delete to authenticated using(user_id=auth.uid());
-- Image uploads require a private or appropriately scoped Supabase Storage bucket
-- with separate object-level policies and file validation. Not included here.
