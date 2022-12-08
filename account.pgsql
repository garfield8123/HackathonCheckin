-- Table: public.account

-- DROP TABLE public.account;

CREATE TABLE IF NOT EXISTS public.account
(
    username text COLLATE pg_catalog."default" NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    dict text COLLATE pg_catalog."default" NOT NULL
)

CREATE TABLE IF NOT EXISTS public.Attendee
(
    "Order #" text COLLATE pg_catalog."default" NOT NULL, 
    "First Name" text COLLATE pg_catalog."default" NOT NULL,
    "Last Name" text COLLATE pg_catalog."default" NOT NULL,
    "Email" text COLLATE pg_catalog."default" NOT NULL,
    "CheckedIn" text COLLATE pg_catalog."default"
    
)