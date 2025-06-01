create table "public"."ownerships" (
    "id" uuid not null default gen_random_uuid(),
    "ownerId" bigint not null,
    "subjectId" bigint not null,
    "active" boolean default false,
    "since" timestamp with time zone,
    "created_at" timestamp with time zone not null default (now() AT TIME ZONE 'utc'::text)
);


alter table "public"."ownerships" enable row level security;

CREATE UNIQUE INDEX ownerships_pkey ON public.ownerships USING btree (id);

alter table "public"."ownerships" add constraint "ownerships_pkey" PRIMARY KEY using index "ownerships_pkey";

grant delete on table "public"."ownerships" to "anon";

grant insert on table "public"."ownerships" to "anon";

grant references on table "public"."ownerships" to "anon";

grant select on table "public"."ownerships" to "anon";

grant trigger on table "public"."ownerships" to "anon";

grant truncate on table "public"."ownerships" to "anon";

grant update on table "public"."ownerships" to "anon";

grant delete on table "public"."ownerships" to "authenticated";

grant insert on table "public"."ownerships" to "authenticated";

grant references on table "public"."ownerships" to "authenticated";

grant select on table "public"."ownerships" to "authenticated";

grant trigger on table "public"."ownerships" to "authenticated";

grant truncate on table "public"."ownerships" to "authenticated";

grant update on table "public"."ownerships" to "authenticated";

grant delete on table "public"."ownerships" to "service_role";

grant insert on table "public"."ownerships" to "service_role";

grant references on table "public"."ownerships" to "service_role";

grant select on table "public"."ownerships" to "service_role";

grant trigger on table "public"."ownerships" to "service_role";

grant truncate on table "public"."ownerships" to "service_role";

grant update on table "public"."ownerships" to "service_role";

create policy "Enable read access for all users"
on "public"."ownerships"
as permissive
for select
to public
using (true);



