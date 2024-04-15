--
-- PostgreSQL database dump
--

-- Dumped from database version 14.10 (Homebrew)
-- Dumped by pg_dump version 14.10 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: anathemacontracts; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.anathemacontracts (
    scroundreladdress character varying(255),
    bribe bigint,
    timedeclared bigint,
    contractaddress character varying(255),
    reason character varying(2000),
    nftindex integer,
    collection character varying(255),
    rarity integer,
    name character varying(255),
    allegiance character varying(255),
    maxpowerpotential bigint,
    maxdefensivepower bigint,
    votingpower bigint,
    overlord character varying(255),
    overlordname character varying(255),
    overlordallegiance character varying(255),
    overlordcollection character varying(255),
    overlordnftindex integer,
    wife character varying(255),
    unique_trait character varying(255),
    members integer,
    overlordrarity character varying(255),
    overlordmembers integer,
    overlordvotingpower integer,
    overlordmaxpowerpotential bigint,
    overlordmaxdefensivepower bigint,
    wartargetname character varying(255),
    overlordwartargetname character varying(255),
    gender character varying(255),
    declareraddress character varying(255),
    declarername character varying(255),
    declarerrarity integer,
    declarerallegiance character varying(255),
    declarernftindex integer,
    declarermembers integer,
    declarervotingpower integer,
    declarermaxpowerpotential bigint,
    declarermaxdefensivepower bigint,
    declarerwartargetname character varying(255),
    declarercollection character varying(255),
    hasrunout boolean,
    revokeraddress character varying(255),
    revokername character varying(255),
    bribepaid boolean,
    revokedbytime boolean,
    overlordnfturi character varying(255)
);


ALTER TABLE public.anathemacontracts OWNER TO esse;

--
-- Name: election; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.election (
    option0 integer,
    option1 integer,
    option2 integer,
    option3 integer,
    option4 integer,
    option5 integer,
    option6 integer,
    option7 integer,
    electionname character varying(255),
    electiondeadline bigint,
    electionstarted bigint,
    electionquestion character varying(2000),
    electionid integer
);


ALTER TABLE public.election OWNER TO esse;

--
-- Name: eventlisteningcheck; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.eventlisteningcheck (
    "time" integer,
    eventcheckstartnumber integer
);


ALTER TABLE public.eventlisteningcheck OWNER TO esse;

--
-- Name: fealtycontracts; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.fealtycontracts (
    lordaddress character varying(255),
    lordsubjectindex integer,
    bribe bigint,
    "time" bigint,
    minimumnftclass integer,
    contractaddress character varying(255),
    campaign character varying(2000),
    nftindex integer,
    collection character varying(255),
    rarity integer,
    name character varying(255),
    allegiance character varying(255),
    maxpowerpotential bigint,
    maxdefensivepower bigint,
    votingpower bigint,
    overlord character varying(255),
    overlordname character varying(255),
    overlordallegiance character varying(255),
    overlordcollection character varying(255),
    overlordnftindex integer,
    wife character varying(255),
    unique_trait character varying(255),
    members integer,
    overlordrarity character varying(255),
    overlordmembers integer,
    overlordvotingpower integer,
    overlordmaxpowerpotential bigint,
    overlordmaxdefensivepower bigint,
    wartargetname character varying(255),
    overlordwartargetname character varying(255),
    gender character varying(255),
    subjectaddress character varying(255),
    subjectname character varying(255),
    hasbeenaccepted boolean,
    item character varying(255),
    magic integer,
    group_attack character varying(255),
    solo_attack character varying(255),
    class character varying(255),
    nfturi character varying(255),
    overlordnfturi character varying(255)
);


ALTER TABLE public.fealtycontracts OWNER TO esse;

--
-- Name: goldcastleeventlisteningcheck; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.goldcastleeventlisteningcheck (
    "time" integer,
    eventcheckstartnumber integer
);


ALTER TABLE public.goldcastleeventlisteningcheck OWNER TO esse;

--
-- Name: goldtokencontractstate; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.goldtokencontractstate (
    lotterybalance numeric,
    warfund numeric,
    airdropbalance numeric,
    wartime integer,
    jackpot numeric,
    datetime bigint
);


ALTER TABLE public.goldtokencontractstate OWNER TO esse;

--
-- Name: goldwithdraw; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.goldwithdraw (
    address character varying(255),
    wonamount bigint,
    datetime integer,
    txid character varying(255),
    jackpot numeric,
    jackpotwinnings numeric
);


ALTER TABLE public.goldwithdraw OWNER TO esse;

--
-- Name: jackpotwinners; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.jackpotwinners (
    address character varying(255),
    jackpotamount bigint,
    datetime integer,
    txid character varying(255)
);


ALTER TABLE public.jackpotwinners OWNER TO esse;

--
-- Name: main_nft_index_sequence; Type: SEQUENCE; Schema: public; Owner: esse
--

CREATE SEQUENCE public.main_nft_index_sequence
    START WITH 1
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.main_nft_index_sequence OWNER TO esse;

--
-- Name: marketplaceeventlisteningcheck; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.marketplaceeventlisteningcheck (
    "time" integer,
    eventcheckstartnumber integer
);


ALTER TABLE public.marketplaceeventlisteningcheck OWNER TO esse;

--
-- Name: marketplacelistings; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.marketplacelistings (
    listingid character varying(255),
    price numeric,
    timelisted bigint,
    nftid character varying(255),
    nftindex integer,
    collection character varying(255),
    rarity integer,
    name character varying(255),
    allegiance character varying(255),
    maxpowerpotential bigint,
    maxdefensivepower bigint,
    votingpower bigint,
    overlord character varying(255),
    overlordname character varying(255),
    overlordallegiance character varying(255),
    overlordcollection character varying(255),
    overlordnftindex integer,
    wife character varying(255),
    unique_trait character varying(255),
    members integer,
    overlordrarity character varying(255),
    overlordmembers integer,
    overlordvotingpower integer,
    overlordmaxpowerpotential bigint,
    overlordmaxdefensivepower bigint,
    wartargetname character varying(255),
    overlordwartargetname character varying(255),
    gender character varying(255),
    item character varying(255),
    nfturi character varying(255),
    bought boolean,
    lister character varying(255)
);


ALTER TABLE public.marketplacelistings OWNER TO esse;

--
-- Name: marriagecontracts; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.marriagecontracts (
    proposeraddress character varying(255),
    dowry bigint,
    "time" bigint,
    contractaddress character varying(255),
    loveletter character varying(2000),
    nftindex integer,
    collection character varying(255),
    rarity integer,
    name character varying(255),
    allegiance character varying(255),
    maxpowerpotential bigint,
    maxdefensivepower bigint,
    votingpower bigint,
    overlord character varying(255),
    overlordname character varying(255),
    overlordallegiance character varying(255),
    overlordcollection character varying(255),
    overlordnftindex integer,
    unique_trait character varying(255),
    magic integer,
    proposergender character varying(255),
    proposee character varying(255),
    members integer,
    overlordmembers integer,
    proposeename character varying(255),
    overlordvotingpower integer,
    overlordmaxpowerpotential bigint,
    overlordmaxdefensivepower bigint,
    overlordwartargetname character varying(255),
    overlordrarity integer,
    offercreatetime bigint,
    hasbeenaccepted boolean,
    maxlovercount integer,
    nfturi character varying(255),
    overlordnfturi character varying(255)
);


ALTER TABLE public.marriagecontracts OWNER TO esse;

--
-- Name: minteventlisteningcheck; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.minteventlisteningcheck (
    "time" integer,
    eventcheckstartnumber integer
);


ALTER TABLE public.minteventlisteningcheck OWNER TO esse;

--
-- Name: nft_goldcastle_asia; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.nft_goldcastle_asia (
    nftindex integer DEFAULT nextval('public.main_nft_index_sequence'::regclass) NOT NULL,
    nftcontractid character varying(255),
    collection character varying(255),
    rarity integer,
    class character varying(255),
    continent character varying(255),
    stars integer,
    title character varying(255),
    domain character varying(255),
    subdomain character varying(255),
    hp integer,
    ap integer,
    magic integer,
    lives integer,
    wisdom integer,
    name character varying(255),
    age integer,
    unique_trait character varying(255),
    solo_attack character varying(255),
    group_attack character varying(255),
    item character varying(255),
    allegiance character varying(255),
    has_secret character varying(255),
    owner character varying(255),
    vote integer,
    votetime bigint,
    wartarget character varying(255),
    warstarted bigint,
    potentialmarriage character varying(255),
    marriagetime bigint,
    feudallord character varying(255),
    feudaltime bigint,
    anathema boolean,
    anathemadeclaredcount integer,
    ismarried boolean,
    issworn boolean,
    isatwar boolean,
    maxpowerpotential bigint,
    nftselfcontractaddress character varying(255),
    maxdefensivepower bigint,
    votingpower integer,
    overlord character varying(255),
    isoverlord boolean,
    nfturi character varying(255),
    gender character varying(255),
    members integer,
    wartargetname character varying(255),
    wife character varying(255),
    overlordname character varying(255),
    feudallordname character varying(255),
    overlordrarity integer,
    anathemareason character varying(2000),
    anathematime bigint,
    anathemadeclarername character varying(255),
    anathemabribe bigint,
    anathemadeclarerrarity integer,
    lovercount integer,
    anathemacooldown bigint,
    vassals integer,
    anathemadeclarer character varying(255),
    overlordnfturi character varying(255),
    overlordallegiance character varying(255)
);


ALTER TABLE public.nft_goldcastle_asia OWNER TO esse;

--
-- Name: nft_goldcastle_asia_nftindex_seq; Type: SEQUENCE; Schema: public; Owner: esse
--

CREATE SEQUENCE public.nft_goldcastle_asia_nftindex_seq
    START WITH 0
    INCREMENT BY 1
    MINVALUE 0
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nft_goldcastle_asia_nftindex_seq OWNER TO esse;

--
-- Name: nft_minting_goldcastle_asia; Type: TABLE; Schema: public; Owner: esse
--

CREATE TABLE public.nft_minting_goldcastle_asia (
    nftindex integer DEFAULT nextval('public.nft_goldcastle_asia_nftindex_seq'::regclass) NOT NULL,
    available boolean
);


ALTER TABLE public.nft_minting_goldcastle_asia OWNER TO esse;

--
-- Data for Name: anathemacontracts; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.anathemacontracts (scroundreladdress, bribe, timedeclared, contractaddress, reason, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, overlordname, overlordallegiance, overlordcollection, overlordnftindex, wife, unique_trait, members, overlordrarity, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, wartargetname, overlordwartargetname, gender, declareraddress, declarername, declarerrarity, declarerallegiance, declarernftindex, declarermembers, declarervotingpower, declarermaxpowerpotential, declarermaxdefensivepower, declarerwartargetname, declarercollection, hasrunout, revokeraddress, revokername, bribepaid, revokedbytime, overlordnfturi) FROM stdin;
\.


--
-- Data for Name: election; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.election (option0, option1, option2, option3, option4, option5, option6, option7, electionname, electiondeadline, electionstarted, electionquestion, electionid) FROM stdin;
0	0	0	0	0	0	0	0	Test Election	1709540619000	1708500619000	About the new collection...	0
\.


--
-- Data for Name: eventlisteningcheck; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.eventlisteningcheck ("time", eventcheckstartnumber) FROM stdin;
\.


--
-- Data for Name: fealtycontracts; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.fealtycontracts (lordaddress, lordsubjectindex, bribe, "time", minimumnftclass, contractaddress, campaign, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, overlordname, overlordallegiance, overlordcollection, overlordnftindex, wife, unique_trait, members, overlordrarity, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, wartargetname, overlordwartargetname, gender, subjectaddress, subjectname, hasbeenaccepted, item, magic, group_attack, solo_attack, class, nfturi, overlordnfturi) FROM stdin;
\.


--
-- Data for Name: goldcastleeventlisteningcheck; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.goldcastleeventlisteningcheck ("time", eventcheckstartnumber) FROM stdin;
\.


--
-- Data for Name: goldtokencontractstate; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.goldtokencontractstate (lotterybalance, warfund, airdropbalance, wartime, jackpot, datetime) FROM stdin;
16989881658950	2500000000000	500000000000	0	1105000000000000000000	\N
16989881658950	2500000000000	500000000000	0	1105000000000000000000	1708121705
\.


--
-- Data for Name: goldwithdraw; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.goldwithdraw (address, wonamount, datetime, txid, jackpot, jackpotwinnings) FROM stdin;
\.


--
-- Data for Name: jackpotwinners; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.jackpotwinners (address, jackpotamount, datetime, txid) FROM stdin;
\.


--
-- Data for Name: marketplaceeventlisteningcheck; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.marketplaceeventlisteningcheck ("time", eventcheckstartnumber) FROM stdin;
\.


--
-- Data for Name: marketplacelistings; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.marketplacelistings (listingid, price, timelisted, nftid, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, overlordname, overlordallegiance, overlordcollection, overlordnftindex, wife, unique_trait, members, overlordrarity, overlordmembers, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, wartargetname, overlordwartargetname, gender, item, nfturi, bought, lister) FROM stdin;
\.


--
-- Data for Name: marriagecontracts; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.marriagecontracts (proposeraddress, dowry, "time", contractaddress, loveletter, nftindex, collection, rarity, name, allegiance, maxpowerpotential, maxdefensivepower, votingpower, overlord, overlordname, overlordallegiance, overlordcollection, overlordnftindex, unique_trait, magic, proposergender, proposee, members, overlordmembers, proposeename, overlordvotingpower, overlordmaxpowerpotential, overlordmaxdefensivepower, overlordwartargetname, overlordrarity, offercreatetime, hasbeenaccepted, maxlovercount, nfturi, overlordnfturi) FROM stdin;
\.


--
-- Data for Name: minteventlisteningcheck; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.minteventlisteningcheck ("time", eventcheckstartnumber) FROM stdin;
\.


--
-- Data for Name: nft_goldcastle_asia; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.nft_goldcastle_asia (nftindex, nftcontractid, collection, rarity, class, continent, stars, title, domain, subdomain, hp, ap, magic, lives, wisdom, name, age, unique_trait, solo_attack, group_attack, item, allegiance, has_secret, owner, vote, votetime, wartarget, warstarted, potentialmarriage, marriagetime, feudallord, feudaltime, anathema, anathemadeclaredcount, ismarried, issworn, isatwar, maxpowerpotential, nftselfcontractaddress, maxdefensivepower, votingpower, overlord, isoverlord, nfturi, gender, members, wartargetname, wife, overlordname, feudallordname, overlordrarity, anathemareason, anathematime, anathemadeclarername, anathemabribe, anathemadeclarerrarity, lovercount, anathemacooldown, vassals, anathemadeclarer, overlordnfturi, overlordallegiance) FROM stdin;
\.


--
-- Data for Name: nft_minting_goldcastle_asia; Type: TABLE DATA; Schema: public; Owner: esse
--

COPY public.nft_minting_goldcastle_asia (nftindex, available) FROM stdin;
\.


--
-- Name: main_nft_index_sequence; Type: SEQUENCE SET; Schema: public; Owner: esse
--

SELECT pg_catalog.setval('public.main_nft_index_sequence', 0, false);


--
-- Name: nft_goldcastle_asia_nftindex_seq; Type: SEQUENCE SET; Schema: public; Owner: esse
--

SELECT pg_catalog.setval('public.nft_goldcastle_asia_nftindex_seq', 471, true);


--
-- Name: nft_goldcastle_asia nft_goldcastle_asia_pkey; Type: CONSTRAINT; Schema: public; Owner: esse
--

ALTER TABLE ONLY public.nft_goldcastle_asia
    ADD CONSTRAINT nft_goldcastle_asia_pkey PRIMARY KEY (nftindex);


--
-- Name: nft_minting_goldcastle_asia nft_minting_goldcastle_asia_pkey; Type: CONSTRAINT; Schema: public; Owner: esse
--

ALTER TABLE ONLY public.nft_minting_goldcastle_asia
    ADD CONSTRAINT nft_minting_goldcastle_asia_pkey PRIMARY KEY (nftindex);


--
-- Name: election unique_electionid; Type: CONSTRAINT; Schema: public; Owner: esse
--

ALTER TABLE ONLY public.election
    ADD CONSTRAINT unique_electionid UNIQUE (electionid);


--
-- PostgreSQL database dump complete
--

