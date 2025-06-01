create table "public"."balances" (
    "id" uuid not null default gen_random_uuid(),
    "userId" bigint not null,
    "amount" bigint default '0'::bigint,
    "updated_at" timestamp with time zone not null default now(),
    "created_at" timestamp with time zone not null default now()
);


alter table "public"."balances" enable row level security;

CREATE UNIQUE INDEX balances_pkey ON public.balances USING btree (id);

CREATE UNIQUE INDEX "balances_userId_key" ON public.balances USING btree ("userId");

alter table "public"."balances" add constraint "balances_pkey" PRIMARY KEY using index "balances_pkey";

alter table "public"."balances" add constraint "balances_userId_key" UNIQUE using index "balances_userId_key";

grant delete on table "public"."balances" to "anon";

grant insert on table "public"."balances" to "anon";

grant references on table "public"."balances" to "anon";

grant select on table "public"."balances" to "anon";

grant trigger on table "public"."balances" to "anon";

grant truncate on table "public"."balances" to "anon";

grant update on table "public"."balances" to "anon";

grant delete on table "public"."balances" to "authenticated";

grant insert on table "public"."balances" to "authenticated";

grant references on table "public"."balances" to "authenticated";

grant select on table "public"."balances" to "authenticated";

grant trigger on table "public"."balances" to "authenticated";

grant truncate on table "public"."balances" to "authenticated";

grant update on table "public"."balances" to "authenticated";

grant delete on table "public"."balances" to "service_role";

grant insert on table "public"."balances" to "service_role";

grant references on table "public"."balances" to "service_role";

grant select on table "public"."balances" to "service_role";

grant trigger on table "public"."balances" to "service_role";

grant truncate on table "public"."balances" to "service_role";

grant update on table "public"."balances" to "service_role";

create policy "Enable read access for all users"
on "public"."balances"
as permissive
for select
to public
using (true);



