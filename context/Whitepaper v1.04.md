# Whitepaper v1.04

## Summary



 
bondifinance.io
Abstract.  The  democratization  of  financial  markets  and  the  advent  of 
tokenization  have  significantly  increased  retail  investors'  access  to 
investment  opportunities.  Bonds,  which  make  up  a  major  portion  of 
global securities markets, play a significant part in this transformation. 
Although  bond  markets  exceed  $100  trillion  in  market  cap,  emerging 
1
market  bonds  constitute  only  25%  of  this  amount,  highlighting  a  big 
gap.   Tokeni...

## Content



 
bondifinance.io
Abstract.  The  democratization  of  financial  markets  and  the  advent  of 
tokenization  have  significantly  increased  retail  investors'  access  to 
investment  opportunities.  Bonds,  which  make  up  a  major  portion  of 
global securities markets, play a significant part in this transformation. 
Although  bond  markets  exceed  $100  trillion  in  market  cap,  emerging 
1
market  bonds  constitute  only  25%  of  this  amount,  highlighting  a  big 
gap.   Tokenized   bonds   offer   improved   liquidity,   lower   transaction 
2
costs,  and  greater  accessibility,  benefiting  investors  and  issuers  alike. 
We   introduce   Bondi,   a   tokenized   bond   protocol   aimed   at   making 
emerging  market  corporate  bonds  available  to  retail  investors,  thereby 
increasing   market   participation   and   liquidity   in   underdeveloped 
financial  systems.  By  October  2023,  the  value  of  tokenized  assets  on 
public   blockchains   had   reached   $118.57   billion,   with   projections 
3
suggesting  it  could  grow  to  between  $3.5  to  $16  trillion  by  2030. As 
4
tokenization is poised for exponential growth, Bondi seeks to capitalize 
on  it  by  addressing  the  challenges  of  illiquid  corporate  bond  issues  in 
emerging markets, promoting financial inclusion and stability. 
 https://www.weforum.org/agenda/2024/03/oecd-government-bonds-and-other-economic-stories-to-read/ 
1
 https://www.ashmoregroup.com/sites/default/files/article-docs/
2
EV_Aug20_3_The_EM_fixed_income_universe_version_9.0.pdf 
 https://www.21.co/research/the-state-of-tokenization
3
 https://cointelegraph.com/news/tokenized-assets-public-blockchains-ripple 
4
  of  132

 
bondifinance.io
Introduction 
From   the   dawn   of   history   until   the   modern   era,   productivity   growth   barely 
surpassed  population  growth  until  the  invention  of  capital  markets.  The  ability  to 
raise funds quickly from a willing group of people changed the world in many ways. 
Fundamentally, this ability is the reason for the world order we know today. 
The  evolution  of  capital  markets  began  in  Europe  in  the  late  13th  century,  the 
concepts   of   joint-stock   companies   and   government   debt   gaining   momentum. 
Stagnating  productivity  had  left  most  people  without  hope  for  a  better  future  and 
excluded most of the population from entrepreneurial ventures. Kings and emperors 
could  only  expand  their  land  and  wealth  at  the  expense  of  their  own  subjects  or 
other  conquered  peoples;  conquests  were  financed  by  former  plunders  or  heavy 
taxation. 
By  the  late  17th  century,  absolute  monarchies  were  weakened,  republics  were 
rising, and subjects were asserting their rights as citizens. 
These  developments  enabled  entrepreneurs  to  raise  funds  easily  and  establish 
flourishing  businesses.  In  some  cases,  debt  issuance  was  preferred  instead  of 
selling  shares,  giving  rise  to  the  need  for  corporate  bonds.     Additionally,  states 
began   borrowing   from   the   public,   offering   interest   in   return,   a   far   more 
advantageous arrangement than imposing burdensome taxes. 
Consequently,  over  the  course  of  500  years,  starting  from  the  1500s,  global 
productivity  per  capita  surged  by  an  impressive  cumulative  1600%,  soaring  from 
$550 to $8800 annually.  
5
 Maddison, A. (2006), The World Economy: Volume 1: A Millennial Perspective and Volume 2: Historical Statistics, 
5
Development Centre Studies, OECD Publishing, Paris, https://doi.org/10.1787/9789264022621-en     
  of  232

 
bondifinance.io
Today,  the  21st  century  is  characterized  by  globalization,  with  the  world  becoming 
increasingly  interconnected.  Borders  are  becoming  less  significant,  and  capital  is 
seeking  new  horizons  to  explore.  Capital  is  plentiful  on  a  global  scale,  and  the 
significance of accessing foreign capital cannot be overstated.  
 
The  tokenization  of  real-world  assets,  particularly  securities,  has  the  potential  to 
propel  the  next  leap  forward,  increasing  widespread  access  to  financial  markets 
around the world. 
Background 
1. Bonds Explained 
Deep   capital   markets   are   essential   for   a   country's   prosperity,   distinguishing 
advanced economies from emerging ones.  
Most  governments  run  budget  deficits,  as  a  result  they  turn  to  debt  markets  to 
finance public infrastructure projects and welfare programs. Similarly, corporations 
constantly need funding to expand their businesses or finance existing operations. 
The debt securities market primarily comprises instruments generally referred to as 
bonds.  These  are  essentially  contracts  where  an  issuer—such  as  a  government, 
municipality, corporation, or other entity borrows funds from investors in exchange 
for  periodic  interest  payments  and  eventual  repayment  of  the  principal  at  an 
agreed-upon  maturity  date.  While  many  traditional  bonds  pay  a  fixed  interest  rate 
(the  coupon)  on  a  set  schedule  until  maturity,  there  is  significant  variation  in  bond 
structures.  Some  bonds  offer  variable  or  floating  interest  rates,  while  others  may  
pay  no  coupon  at  all  (zero-coupon  bonds)  and  instead  are  issued  at  a  discount  to 
their face value. Additionally, certain bonds can be callable, puttable, convertible  
  of  332

 
bondifinance.io
into equity, or tied to inflation or other economic indicators. In general, at maturity, 
most  bonds  return  the  initial  principal  amount  (often  referred  to  as  the  par  or  face 
value),  though  the  terms  and  conditions  differ  widely  depending  on  the  specific 
type of bond. 
2. Importance of Bonds In Corporate Financing 
Corporate  bonds  are  important  financial  instruments  for  both  companies  and 
investors.  They  provide  companies  with  a  reliable  means  of  raising  capital  without 
diluting  ownership,  as  would  occur  with  equity  financing.  For  investors,  corporate 
bonds  offer  a  relatively  stable  and  predictable  income  stream,  with  the  added 
benefit  of  priority  over  equity  holders  in  the  event  of  issuer  default.  This  makes 
corporate  bonds  an  attractive  investment  option,  especially  in  uncertain  economic 
times when equity markets are volatile. 
In  addition  to  providing  a  desirable  investment  venue  for  retail  investors,  a  well-
diversified  and  liquid  bond  market  is  crucial  to  meet  the  capital  needs  of  the 
corporate sector which, in emerging markets, still relies heavily on foreign financial 
markets  and  bank  financing.  An  established  bond  market  expands  the  pool  of 
potential  investors,  including  sovereign  wealth  funds,  life  insurers,  and  pension 
funds,  which  are  better  equipped  to  provide  stable,  long-term  financing  compared 
to traditional banks.   
678
 Surti, Jay, and Rohit Goel. "CHAPTER 5 Corporate Debt Market: Evolution, Prospects, and Policy". India’s Financial 
6
System. USA: International Monetary Fund, 2023. < https://doi.org/10.5089/9798400223525.071.CH005>. Web. 29 Jul. 
2024
 World Bank. 2012. Turkey - Corporate Bond Market Development : Priorities and Challenges. © Washington, DC. 
7
http://hdl.handle.net/10986/12439 License: CC BY 3.0 IGO
 Attila Becsi & Gergely Bognar & Mate Loga, 2021. "The Growing Importance of the Economic Role of the Corporate 
8
Bond Market," Financial and Economic Review, Magyar Nemzeti Bank (Central Bank of Hungary), vol. 20(4), pages 5-37
  of  432

 
bondifinance.io
This  diversification  is  particularly  critical  in  times  of  financial  distress  when  banks 
may drastically cut back on lending, as seen during the 2008 Financial Crisis when 
loan  issuance  to  large  borrowers  dropped  by  79%  from  peak  levels. A self 
9
sufficient  bond  market  supplements  the  financial  independence  and  freedom  of 
emerging markets in times of stagnant or recessive global economic conditions. 
Additionally,   borrowing   with   bonds   tend   to   give   companies   more   desirable 
conditions for their loans. The covenants of bonds tend to be less restrictive for the 
issuers,  and  on  average,  bonds  have  longer  maturity  profiles  compared  to  bank 
loans. 
10
3. Size and Growth 
Globally, the market cap of bond markets was estimated to be between $100 trillion 
and  $129.8  trillion  in  2023,  comparable  in  size  to  both  global  GDP  and  the  global 
equities market.   
1112
In the US, the outstanding value of bonds reached $51.9 trillion in 2023, surpassing 
the equity market's value of $40.3 trillion and increasing more than double by $30 
trillion  since  2008.   Notably,  the  share  of  bonds,  particularly  corporate  bonds, 
1314
relative  to  other  financing  types  has  also  increased  significantly.  Corporate  bonds 
accounted for 34% of US corporate debt financing in 2023, up from 19% in 2000. 
15
 Victoria Ivashina, David Scharfstein, Bank lending during the financial crisis of 2008, Journal of Financial Economics, 
9
Volume 97, Issue 3, 2010, Pages 319-338, ISSN 0304-405X, https://doi.org/10.1016/j.jfineco.2009.12.001 
 Cortina, Juan J., Tatiana Didier, and Sergio L. Schmukler. Corporate Borrowing and Debt Maturity: Market Access and 
10
Crisis Effects. January 2018.
 https://www.weforum.org/agenda/2024/03/oecd-government-bonds-and-other-economic-stories-to-read/ 
11
 https://www.sifma.org/resources/research/fact-book/ 
12
 https://www.sifma.org/resources/research/fact-book/ 
13
 https://www.oecd.org/en/publications/2024/03/global-debt-report-2024_84b4c408.html
14
 Suresha S. (2023). Corporate bonds vis-a-vis bond market: Global economy. The Scientific Temper, 14(3):1014-1019 
15
  of  532

 
bondifinance.io
Globally, the importance of corporate bond markets has also increased since 2008. 
Corporate  bonds  accounted  for  19%  of  worldwide  non-financial  corporate  debt  in 
2023,  up  from  10%  in  2007 Braun  et  al.,  2008.  The  increase  in  the  share  of 
corporate   bonds   in   corporate   financing   has   been   even   more   pronounced   in 
emerging markets. In China, bond financing for corporate debt increased from 1% to 
11% between 2001 and 2011. In Brazil, the increase was from 5% to 25%. 
16
These figures highlight the growing relevance of corporate bonds over the last two 
decades.  The  increasing  share  of  corporate  bonds  in  debt  financing  underscores 
their rising demand and importance in 2023, particularly in emerging markets. 
Globally,  non-financial  corporations  have  increased  their  bond  issuance  nominally 
too. Corporate bonds have grown 2.7 times since 2007 to $11.7 trillion in worldwide 
value, tripling compared to global GDP increase. Yet, developing nations saw only a 
1.92 times increase from $85 billion in 2007 to $164 billion in 2017. 
17
Although   corporate   bonds   disproportionately   increased   their   market   share   in 
corporate   financing   in   emerging   markets,   nominal   corporate   bond   issuance 
increased proportionally less than world average.  
Furthermore,  overall  indebtedness  as  a  percentage  of  GDP  remains  approximately 
twice   as   high   for   advanced   economies   compared   to   emerging   markets   and 
developing countries EMDC. 
18
In  2012,  bond  markets  in  the  U.S.  and  other  developed  economies  accounted  for 
222%  and  109%  of  GDP,  respectively,  with  bonds  excluding  government  bonds 
representing  135%  and  63%  of  GDP.  Conversely,  in  India,  other  emerging  Asian 
countries, and Africa, bond markets comprised 34%, 42%, and 39% of GDP,  
 Suresha S. (2023)
16
 Suresha S. (2023)
17
 Xiang Fang & Bryan Hardy & Karen Lewis, 2023. "Who holds sovereign debt and why it matters," BIS Working 
18
Papers 1099, Bank for International Settlements
  of  632

 
bondifinance.io
respectively,  while  bonds  excluding  government  bonds  represented  a  mere  8%, 
13%,  and  6%  of  GDP.  Notably,  by  2020,  India's  bond  market  had  grown  to  47%  of 
GDP. 
19
4. Challenges in the Bond Markets 
While technological advancements enabled retail investors to significantly increase 
their  participation  in  global  financial  markets.  There  are  still  significant  obstacles 
that prevent them from fully accessing fixed-income assets. 
Unlike equities, bonds lack efficient trading venues. Most transactions are done via 
OTC  deals,  which  reduce  the  overall  desirability  of  bond  investing.  OTC  deals    are 
particularly  harmful  to  the  development  of  the  market  because  they  promote 
information   asymmetry   and   increase   transaction   costs   thanks   to   the   high 
involvement of intermediaries in transactions. 
While   corporate   bonds   issued   by   companies   from   advanced   economies   with 
developed  bond  markets  usually  allow  trading  in  smaller  denominations  of  around 
$1000,   a   large   majority   of   emerging   market   corporate   bonds   have   minimum 
settlement  values  of  above  $100,000  which  makes  them  extremely  illiquid  and 
inaccessible.  The  illiquidity  issue  for  these  bonds  is  so  dire  that  even  hedge  funds 
and  other  asset  managers  consider  the  illiquidity  risk  as  a  considerable  concern 
when  taking  investment  decisions  that  involve  these  instruments.  In  a  landscape 
that  so  heavily  discourages  even  investors  with  large  amounts  of  capital,  retail 
investors are almost completely left out. 
Additionally, there are other persistent issues that prevent better integration of retail 
investors.   The   current   public   issue   requirements   are   often   perceived   as   too 
onerous, counter-productive, and time-consuming. As a result, in many emerging  
 ASIFMA Paper: India Bond Market Roadmap - October 2013
19
  of  732

 
bondifinance.io
and  underdeveloped  economies,  the  private  placement  route  is  still  preferred  by 
most   corporate   bond   issuers.   Private   placements   lack   the   transparency   and 
statutory disclosure obligations associated with public offerings. Since a significant 
share  of  the  market  is  dominated  by  a  select  group  of  institutional  repeat  players, 
market dynamics are influenced more by mutual trust and reputational factors than 
by  regulatory  oversight.  The  lack  of  standardization  and  overall  opacity  in  private 
placements  can  be  attributed  to  these  dynamics.  Furthermore,  since  privately 
placed  bonds  are  typically  held  by  investors  until  maturity,  they  fail  to  provide  the 
necessary  liquidity  in  the  secondary  market,  significantly  affecting  the  growth  of 
corporate debt markets in emerging and underdeveloped countries. 
20
The  common  practice  in  advanced  economies  is  to  proceed  with  public  issues 
wheres  private  placements  play  a  major  part  in  emerging  markets.  In  Vietnam  and 
India,  approximately  90%  to  99%  of  the  existing  bonds  are  issued  through  private 
placements. However, private placements accounted for only 12% in the USA, 10% 
in Germany, and 0.4%  15% in South Korea.   
2122
5. Financial Inclusion and Bond Markets 
According  to  the  United  Nations  Capital  Development  Fund UNCDF,  financial 
inclusion  involves  providing  individuals  and  enterprises  with  access  to  a  range  of 
appropriate   and   responsibly   offered   financial   services   within   a   regulated 
framework.   Financial   inclusion   is   a   key   driver   of   economic   development.   By 
providing broader access to financial products and services, it improves the overall 
stability and growth of financial systems. 
 Schou-Zibell, Lotte & Wells, Stephen, 2008. "India's Bond Market-Developments and Challenges Ahead," Working 
20
Papers on Regional Economic Integration 22, Asian Development Bank
 MB Securities Joint Stock Company, Vietnam Bond Market In the Readiness for Further Growth
21
 https://www.livemint.com/money/personal-finance/increasing-retail-investor-participation-in-corporate-bonds-the-
22
case-for-a-smaller-ticket-size-11696785149518.html 
  of  832

 
bondifinance.io
A strong debt market, with a balanced distribution between bank loans and bonds, 
is crucial for a robust economy. When a large corporate bond market is established, 
it  allows  market  dynamics  to  play  a  larger  role  in  the  economy,  which  helps  in 
lowering  systemic  risk  and  preventing  financial  crises.  This  environment  promotes 
better  accounting  transparency,  a  strong  network  of  financial  analysts,  credible 
rating  agencies,  and  a  variety  of  corporate  debt  instruments  and  derivatives  that 
require  advanced  credit  analysis.  It  also  ensures  efficient  processes  for  corporate 
restructuring and liquidation. All these mechanisms, born out of necessity for the 
23
efficient  working  of  bond  markets,  naturally  result  in  the  growth  of  the  financial 
system, therefore improving financial inclusion. 
In  the  US,  households  hold  19%  of  all  corporate  bonds  and  the  remaining  81%  is 
held by institutional investors, banks and other legal entities.  
In Japan, for instance, only 5% of the total outstanding amount of corporate bonds 
was  held  by  households  at  the  end  of  2013.  In  Japan,  the  largest  investors  by  far 
were  the  banks  and  other  financial  institutions,  including  the  financial  institutions 
for small businesses, with 53% of the total amount. 
Direct  holdings  of  bonds  by  individual  investors  nevertheless  vary  a  lot  between 
European countries. In Italy, individual investor holdings of bonds comprise 20% or 
more of total financial holdings. In Germany, the equivalent percentage is between 
10  15%, and in other countries it will be typically lower than 5% the lowest figure 
being that for the UK (just 1.5%. 
A  survey  by  IOSCO 2011)  on  corporate  bond  markets  in  36  emerging  market 
economies showed that the share of retail investors was 9% in 2010. This figure is 
higher  than  many  of  the  advanced  economies,  displaying  the  demand  for  these 
products in emerging markets. 
24
  Hakansson, Nils H., The Role of a Corporate Bond Market in an Economy--And in Avoiding Crises (June 1999). IBER 
23
RPF-287, Available at SSRN: https://ssrn.com/abstract=171405 or http://dx.doi.org/10.2139/ssrn.171405
 Çelik, S., G. Demirtaş and M. Isaksson (2015), "Corporate Bonds, Bondholders and Corporate Governance", OECD 
24
Corporate Governance Working Papers, No. 16, OECD Publishing, Paris, https://doi.org/10.1787/5js69lj4hvnw-en. 
  of  932

 
bondifinance.io
Introducing Bondi 
Tokenized  bonds  mark  a  significant  advancement  in  financial  technology,  offering 
greater accessibility, lower costs, and more liquidity than traditional bonds. 
By  using  tokenization,  platforms  like  Bondi  remove  barriers  to  entry  for  retail 
investors  by  allowing  bond  purchases  from  as  little  as  $100.  This  broader  access 
helps diversify the investor base and fosters greater financial inclusion. Individuals 
who  were  once  deterred  by  high  minimum  investment  requirements  can  now 
participate in the bond market, expanding its appeal. 
Issuance  and  trading  costs  are  also  reduced  through  tokenization.  In  contrast  to 
traditional   bonds   that   involve   multiple   intermediaries   and   lengthy   paperwork, 
tokenized bonds use smart contracts and automated processes that limit expenses. 
Underwriting fees, for example, decrease on average by 0.22 percentage points of 
the   bond’s   par   value,   translating   to   a   25.8   percent   reduction   compared   to 
conventional bonds. Issuers can also offer tokenized bonds at a yield spread that is 
0.78  percentage  points  lower  than  that  of  similar  conventional  bonds,  reflecting  a 
23.9  percent  reduction  at  issuance.  These  cost  savings  benefit  both  issuers  and 
investors. 
Liquidity  improves  as  well.  Bid  ask  spreads  for  tokenized  bonds  decrease  by  an 
average  of  0.035  percentage  points,  representing  a  5.3  percent  reduction.  The 
benefit becomes even more pronounced when retail investors participate, reaching 
a  10.8  percent  decrease.  Furthermore,  the  presence  of  tokenized  bonds  can 
increase the liquidity of an issuer’s conventional bonds, resulting in an average bid 
ask spread reduction of 0.049 percentage points, or 8.5 percent, after the issuance 
of a similar tokenized bond. 
25
 Institute for Monetary and Financial Research, Hong Kong, An Assessment on the Benefits of Bond Tokenisation 
25
(November 2023). Hong Kong Institute for Monetary and Financial Research (HKIMR) Research Paper 17/2023, 
Available at SSRN: https://ssrn.com/abstract=4624156 or http://dx.doi.org/10.2139/ssrn.4624156 
  of  1032

 
bondifinance.io
Lower  transaction  costs  also  encourage  more  frequent  trading  and  support  better 
price  discovery.  As  a  result,  both  tokenized  and  conventional  bonds  trade  under 
more  favorable  conditions,  allowing  a  wider  range  of  investors  to  participate  and 
benefit. 
	Institute for Monetary and Financial Research, Hong Kong, 2023

Bond Tokens  
Bondi’s  Bond  Tokens BTs  are  self-custodial,  ERC20  compatible  tokens  fully 
backed   by   the   bonds   they   represent.   While   they   can   be   transferred 
permissionlessly,  actions  that  require  interactions  with  the  real  world  such  as 
minting, claiming coupon payments, and burning tokens at maturity to redeem their 
face  value  require  identity  verification  to  ensure  regulatory  compliance.  Each  BT 
corresponds to a specific bond, with a fixed face value of $100. The tokens follow a 
naming  convention  of  “btXXX,” where “XXX”  reflects  the  first  word  of  the  issuer’s 
name.  BTs  are  designed  to  retain  all  the  benefits  of  holding  traditional  corporate 
bonds   while   introducing   the   improved   flexibility   and   efficiency   offered   by 
tokenization. 
  of  1132

 
bondifinance.io
The  most  important  feature  of  BTs,  by  far,  is  the  fractionalization  of  the  underlying 
asset. The majority of USD-denominated emerging market corporate bonds have a 
minimum  settlement  value  exceeding  $100,000.  With  a  face  value  of  $100  and  a 
minimum  tradable  unit  of  18  decimals,  BTs  significantly  improve  efficiency  on  the 
liquidity front. 
Verification Requirements 
There  are  three  actions  that  a  BT  holder  can  interact  with  traditional  markets  and 
require KYC  
A.Minting 
Bondi  issues  Bond  Tokens BTs  through  a  process  that  begins  with  pooling  user 
funds in smart contracts known as “funding contracts.” These contracts serve as an 
offering  period  during  which  users  commit  their  funds  to  the  funding  phase.  Once 
the  target  amount  is  reached,  the  pooled  funds  are  used  to  purchase  bonds  in 
traditional  markets,  and  Bond  Tokens  are  subsequently  minted  and  distributed  to 
participants   (see   the   Primary   Market   section   for   a   detailed   explanation).   To 
participate in a funding phase, users must first verify their identities by completing 
the  KYC  process  via  Bondi’s  User  Dashboard.  Once  verified,  the  user’s  connected 
wallet is whitelisted, making it eligible to participate in funding phases. Importantly, 
any  wallet  approved  to  join  a  funding  phase  is  automatically  authorized  to  mint  its 
Bond Tokens during the minting phase without requiring additional verification. 
B. Claiming Coupons 
On   the   bond’s   coupon   dates,   Bondi   receives   the   coupon   payments   into   its 
brokerage account. Once received, these payments are converted to USDC through 
Bondi’s  partners  and  deposited  into  the  coupon  disbursement  smart  contract.  Any 
wallet holding Bond Tokens is entitled to claim a proportional share of the coupon  
  of  1232

 
bondifinance.io
payment based on the amount of tokens it holds. While Bond Tokens can be freely 
traded   on   secondary   markets   in   a   permissionless   manner,   claiming   coupon 
payments   requires   the   wallet   owner   to   complete   KYC   verification   to   ensure 
compliance with regulations. 
C. Redeeming the Principal 
At  the  bond’s  maturity  date,  the  final  coupon  payment  and  the  face  value  are  paid 
by  the  issuer.  These  funds  are  then  converted  into  USDC  and  deposited  into  the 
burning smart contract. The burning smart contract works similar to the coupon  
smart contract with one difference being the condition of burning the BTs to be able 
to claim the principal. Once the funds are available in the contract, BT holders who 
have  completed  KYC  can  burn  their  tokens  to  redeem  the  principal  amount  along 
with the last coupon payment. 
Call Feature 
The call function of Bond Tokens BTs ensures that actions taken by bond issuers 
in  traditional  markets,  such  as  early  redemptions,  are  reflected  onchain  for  token 
holders.  In  bond  markets,  bond  issuers  may  exercise  their  right  to  redeem  bonds 
before maturity on specific call dates at predetermined prices. For example, a bond 
maturing  in  June  2028  might  have  call  dates  in  June  2025  at  $103,  June  2026  at 
$102,   and   June   2027   at   $101.   The   issuer   can   choose   to   redeem   the   entire 
outstanding amount on any of these dates or allow the bond to reach maturity. 
If  the  issuer  opts  for  a  partial  redemption,  a  set  percentage  of  the  outstanding 
amount—such as 25%—may be redeemed on a given call date. Some bonds include 
additional   clauses   limiting   the   percentage   or   specifying   conditions   for   early 
redemption. Bondi ensures that these traditional market actions are mirrored  
  of  1332

 
bondifinance.io
onchain  by  executing  a  forced  transfer  of  the  corresponding  BTs  from  token 
holders, effectively retiring the tokens that represent the redeemed bonds. Token  
holders   are   able   to   claim   the   compensation   of   their   retired   BTs   from   the 
compensation smart contract by connecting to the User Dashboard. 
Document Append Feature 
The document append feature for Bond Tokens ensures that all critical bond-related 
documents,  such  as  prospectuses  and  brokerage  statements  for  purchasing  and 
holding  the  underlying  bonds,  are  accessible  and  verifiable.  This  feature  also 
supports  updates,  enabling  new  documents  to  be  appended  while  preserving  a 
record of previous versions. 
Actors 
The  ecosystem  consists  of  four  main  actors:  the  protocol,  the  custodian  broker, 
primary market investors, and secondary market investors.  
1.Bondi 
Bondi  serves  as  the  platform  where  the  primary  and  secondary  markets  for  Bond 
Tokens BTs  operate.  During  Phase  1,  the  protocol  facilitates  the  funding  and 
minting  processes,  enabling  users  to  pool  funds  through  smart  contracts  until  a 
target  investment  amount  is  reached.  Once  funded,  Bond  Tokens  are  minted  and 
distributed to investors. In Phase 2, the protocol will introduce steadyAMMs, which 
will  allow  users  to  trade  BTs  on  a  secondary  market,  ensuring  liquidity  and  market 
accessibility. To maintain compliance, the protocol only allows verified users to mint 
tokens, claim coupons, or redeem bond principal. 
  of  1432

 
bondifinance.io
Key functionalities include: 
•Onboarding:  Users  complete  identity  verification  to  gain  access  to  the  primary 
market, ensuring that all participants meet compliance requirements. 
•User Dashboard: Investors can manage their holdings, access live data, and claim 
their coupon payments or bond principal when due. 
•Offboarding:  At  maturity,  verified  users  can  redeem  their  tokens  in  exchange  for 
the bond’s face value and final coupon payment. 
2. Custodian Broker 
The custodian broker acts as the link between traditional markets and the Bondi. It 
is  responsible  for  acquiring  the  bonds  once  a  funding  phase  is  complete,  holding 
them on behalf of the protocol, and ensuring accurate disbursement of coupon and 
principal  payments.  The  broker  also  delivers  regular  audit  reports  to  maintain 
transparency and trust. 
3. Primary Market Investor 
Primary market investors are participants in the funding phases, where they commit 
funds  to  mint  Bond  Tokens.  Once  minted,  these  investors  hold  the  rights  to  the 
bond’s coupon payments and principal value at maturity. If they decide to exit their 
positions  before  maturity,  they  can  sell  their  tokens  on  the  secondary  market. 
Investors who partially sell retain the right to earnings on their remaining holdings. 
  of  1532

 
bondifinance.io
4. Secondary Market Investor 
Secondary market investors engage with Bond Tokens after they have been minted 
and   made   available   for   trading   on   the   protocol’s   exchange,   powered   by   the 
steadyAMM.   The   steadyAMM   provides   a   decentralized   and   efficient   trading 
mechanism,  allowing  investors  to  buy  and  sell  Bond  Tokens  freely.  Unlike  primary 
market  participants,  secondary  market  investors  are  not  required  to  complete 
identity verification, provided their wallets are not blacklisted. The steadyAMM also 
enables price stability and seamless transactions, making it easier for new investors 
to enter the market and for existing holders to exit their positions as needed. 
Mechanisms 
1.The Primary Market 
The  primary  market  is  where  the  initial  funding  for  each  bond  issue  takes  place. 
Participation  is  open  only  to  investors  who  have  completed  the  required  identity 
verification   through   the   User   Dashboard.   Once   verified,   these   investors   can 
contribute  a  minimum  of  $100  during  a  predetermined  funding  window—e.g.,  30 
days—to  help  meet  a  specified  target  amount.  If,  for  example,  the  target  is  set  at 
$200,000,  participants  have  until  the  deadline  to  collectively  reach  or  surpass  this 
total. 
If the target amount is achieved in time, the pooled funds are then used to purchase 
the  bonds  from  a  regulated  custodian  broker.  Should  the  target  not  be  met  by  the 
deadline, the smart contracts automatically return all contributed funds to investors, 
ensuring that no participant is penalized for an unsuccessful funding round. 
  of  1632

 
bondifinance.io
Clean and Dirty Prices 
It  is  important  to  recognize  that  bonds  are  bought  at  their  “dirty  price,”  which 
consists   of   the   clean   price   (the   base   valuation)   plus   any   accrued   interest 
accumulated since the bond’s last coupon payment. While the target amount—such 
as  $200,000—reflects  the  intended  clean  price  allocation,  the  funding  mechanism 
also   accounts   for   the   accrued   interest.   This   additional   amount   is   collected 
proportionally  from  all  participants,  ensuring  that  each  investor  shares  fairly  in  the 
full acquisition cost of the bonds. 
Under  traditional  market  conditions,  an  investor  purchasing  bonds  directly  would 
pay  the  accrued  interest  owed  only  at  the  specific  moment  of  settlement.  By 
contrast,  the  funding  approach  spreads  the  bond  acquisition  over  a  set  period, 
meaning that early participants commit their funds before the final purchase date. 
In effect, these early contributors are covering accrued interest that is not yet fully 
realized  at  the  time  they  invest.  Meanwhile,  those  who  join  closer  to  the  deadline 
effectively  pay  accrued  interest  that  matches  the  settlement  day  more  closely.To 
counterbalance this timing disadvantage faced by early participants, Bondi awards 
additional incentive points to those who commit their funds sooner. 
The Funding Phase 
Let   represent the target investment amount for a given bond issue. For example, if 
 , this value corresponds to the bond’s clean price. Investors participate 
by contributing funds into a single, continuous funding window—say, over 30 days
—until  the  target  amount  is  reached.  Each  investor  must  commit  at  least  $100, 
ensuring meaningful participation while keeping the barrier to entry manageable. 
T
T=$200,000
  of  1732

 
bondifinance.io
Let    denote  the  contribution  of  the  -th  investor,  with  a  total  of   investors. Thus, 
the total contributions at any point can be expressed as: 
  
2. The Secondary Market, steadyAMM 
The  steadyAMM  serves  as  an  exchange  that  enables  the  trading  of  bond  tokens. 
Since  the  bond  tokens  cannot  be  redeemed  before  maturity,  primary  market 
investors who want to exit their positions have to use the secondary market to sell 
their  tokens.  It  has  a  permissionless  structure,  providing  a  DeFi-like  experience 
where  prospective  investors  may  simply  connect  their  wallets  (as  long  as  they  are 
not blacklisted) and conduct trades. 
The  constant  product  formula  of  Automated  Market  Makers AMMs is used to 
determine  the  price  of  two  assets  in  relation  to  each  other  mathematically.  The 
formula ensures that the product of the quantities of two tokens in the liquidity pool 
remains constant. This formula is represented as: 
  
where: 
•   is the quantity of token   (e.g., bond token) in the liquidity pool. 
•   is the quantity of token   (e.g., a stablecoin) in the liquidity pool. 
•  is a constant that remains unchanged. 
Although the well-known constant product function dictates the price changes, we 
propose  two  key  modifications  to  the  standard  constant  product  function  for  the 
purpose of trading bond tokens: 
C
i
in
n
∑
i=1
C
i
x⋅y=k
xX
yY
k
  of  1832

 
bondifinance.io
A.Price Boundaries 
We  recognize  that  bond  tokens  may  exhibit  limited  liquidity  at  the  beginning, 
potentially   leading   to   significant   price   discrepancies   between   the   protocol’s 
secondary market prices and the real-world market prices. To ensure price stability, 
we  integrate  circuit  breakers  when  prices  reach  5%  of  the  oracle  price,  only 
allowing  trades  on  the  opposite  direction.  The  oracle  price  is  fetched  from  live 
market data. 
To  maintain  the  price  of  the  Bond  Tokens  within  5%  of  the  oracle  price,  the 
following boundaries are defined: 
 Oracle Price  : The price of the bond tokens provided by the oracle. 
 Upper Bound  :   
 Lower Bound  :   
Mechanism for Maintaining Price Range 
1.Initialization 
Users  provide  liquidity  with  initial  quantities   and    such  that  the  initial 
price of   equals the oracle price  : 
  in terms of   
±
±
P
o
P
max
P
max
=1.05⋅P
o
P
min
P
min
=0.95⋅P
o
x
bondtoken
y
usd
XP
o
P
o
=
y
usd
x
bondtoken
Y
  of  1932

 
bondifinance.io
2. Regular Supply and Price Calculation 
Supply Dynamics 
   
  
Price Calculation 
     
3. Trade Execution and Price Bound Adjustments 
When Buying Bond Tokens 
Calculate   to ensure that it remains within the upper bound: 
  
When Selling Bond Tokens 
Calculate   to ensure that it remains within the lower bound: 
  
The circuit breaker will be activated if   does not satisfy the conditions. 
Note that the above calculations of price and supply do not account for the accrued 
coupon interest to which each bond is entitled. The modified calculation will not  
Δx
bondtoken
=amount bought (-), or sold (+)
Δy
usd
=
k
x
bondtoken
+Δx
bondtoken
−y
usd
X
=
y
usd
+Δy
usd
x
bondtoken
+Δx
bondtoken
Y
P
new
P
new
=
y
usd
+Δy
usd
x
bondtoken
+Δx
bondtoken
≤P
max
P
new
P
new
=
y
usd
+Δy
usd
x
bondtoken
+Δx
bondtoken
≥P
min
P
new
  of  2032

 
bondifinance.io
change the formula of    but will change its numerical outcome. This is discussed 
in the following section. 
B. Accrued Interest 
Accrued  interest  refers  to  the  interest  earned  on  a  bond  but  not  yet  collected. 
Interest  accumulates  from  the  bond's  issuance  or  coupon  date  until  the  next 
coupon  date  or  maturity  date.  When  buying  or  selling  a  bond  through  a  broker, 
accrued  interest  is  either  credited  to  or  debited  from  your  account  automatically. 
The  steadyAMM  model  incorporates  accrued  interest  into  the  supply  and  price 
calculations by integrating it into the pool, similar to traditional market practices. 
Bond Token Sale 
When  an  investor  sells  their  bond  tokens  on  the  secondary  market  between  two 
coupon dates, the  pool pays the the accrued interest they earned during the period 
they held the tokens in addition to the market price.  
Bond Token Purchase  
When an investor buys tokens on the secondary market between two coupon dates, 
they pay the the accrued interest to the pool, accounting for the accrued interest of 
the liquidity provider’s tokens. 
  
Adjusted Supply Dynamics of the AMM 
  = accrued coupon: paid to the pool (+), paid from the pool (-) 
   
  
P
new
Accrued Interest=
(
Coupon Rate
Number of Coupons per Year
)
×
(
Days Since Last Coupon
Days in Coupon Period
)
Δc
Δx
bondtoken
=amount bought (-), or sold (+)
Δy
usd
=
k
x
bondtoken
+Δx
bondtoken
−y
usd
+Δc
  of  2132

 
bondifinance.io
As   is calculated using the    and   values determined by this adjustment, this 
does not alter the   formula above. 
3. Coupon Disbursements 
The  bond  tokens  allow  their  holders  to  redeem  coupon  payments  from  the  user 
dashboard when the date comes. A token holder does not have to hold a full token 
to redeem a coupon payment, a fractional owner can redeem coupon payments that 
correspond to their portion of a bond. 
To qualify for coupon redemption, investors must meet the following requirements: 
•
The  coupon  an  investor  can  claim  corresponds  to  the  amount  of  tokens  they 
hold at the time of the coupon date. 
•
Only token holders who have a registered wallet are eligible. 
4. Credit Rating System 
Traditional  credit  rating  systems  may  fall  short  due  to  biases  and  inadequacies  in 
assessing  the  unique  conditions  of  emerging  markets.  Furthermore,  traditional 
credit  ratings  tend  to  constrain  the  rating  with  “sovereign-ceiling”,  which  limits  the 
highest  credit  rating  a  corporate  issuer  can  receive  to  the  sovereign  rating  of  the 
country in which it is located.  
26
To evaluate the potential yield and credit risks posed by emerging market corporate 
bonds  more  accurately,  we  have  developed  the  Bond  Spectrum  Model,  a  revised 
version  of  the  modified  ZScore model developed by NYU Stern Finance Professor 
Edward Altman. The original Z-score model, which was also invented by Altman,  
P
new
ΔyΔx
P
new
Altman, Edward. (2005). An emerging market credit scoring system for corporate bonds. Emerging Markets Review. 6. 
26
311-323. 10.1016/j.ememar.2005.09.007
  of  2232

 
bondifinance.io
incorporates  certain  financial  metrics  with    corresponding  coefficients  depending 
on   how   much   each   affects   the   bankruptcy   probability   of   US   manufacturing 
companies.  Altman  later  proposed  a  modified  ZScore,  named  Emerging  Market 
Score EMS,    applicable  to  emerging  market  corporations  from  all  industries.  The 
EMS  equation  involves  different  financial  metrics  and  coefficients,  tailored  to  the 
bankruptcy risk factors relevant to these markets.  
  
where  ,  ,  , and 
  
In  the  EMS  model,  a  US  equivalent  firm  must  have  been  rated  with  the  same 
methodology to establish a rating for an emerging market firm. For this, a roster of 
US  debt  issuers  are  first  scored  according  to  EMS Table  2.  After  that,  the  EMS 
scores of the companies are matched with the credit ratings they received from  
credit  rating  agencies  to  establish  a  benchmark  for  each  score.  To  letter-rate  an 
emerging  market  firm,  its  EMS  score  is  calculated,  and  the  firm  is  given  the 
corresponding  letter  grade  of  a  US  firm  with  the  same  EMS  score.  The  final  credit 
rating  reached  by  the  EMS  model Modified  Rating  Column  on  Table  1)  is  the  letter 
grade  obtained  above,  adjusted  by  notches  based  on  company  and  emerging 
market specific criteria. 
  
EMS=6.56×X
1
+3.26×X
2
+6.72×X
3
+1.05×X
4
+3.25
X
1
=
Working capital
Tot al assets
X
2
=
Retained earnings
Tot al assets
X
3
=
Operating income
Tot al assets
X
4
=
Book value of equity
Tot al liabilities
  of  2332

 
bondifinance.io
 Table 1 
Table  1 exhibits the letter grades which the evaluated firms received under Altman’s 
EMS model compared to the ratings they received from the “big three” credit rating 
agencies.  The  “Modified  Rating”  column  displays  the  rating  results  from  Altman’s 
model. Meanwhile, The “Ratings M/S&P/D&P” column displays the ratings given by 
the  credit  rating  agencies.  The  effects  of  credit  rating  agency  bias  is  clear,  as 
Altman’s model rated the firms significantly higher. 
In addition to notch adjustments according to company-specific circumstances, we 
propose  one  new  adjustment  criterion  and  modify  the  use  of  the  existing  but 
unquantifiable US corporate - EM sovereign yield differential. 
   
  of  2432

 
bondifinance.io
  Table 2 
A. The Bond Spectrum Model 
We  offer  an  innovative  approach  to  credit  ratings  by  establishing  a  color-rated 
system.  This  system  is  designed  to  be  more  user-friendly  by  simplifying  complex 
letter-rated systems.  
The  color  spectrum  corresponds  to  numbers  between  0100.  In  order  to  achieve 
this using the EMS model, we need to normalize the EMS as well as the modification 
parameters, which are notches. 
  of  2532

 
bondifinance.io
To calculate the normalized EMS,  we use the following formula: 
 , where 
   
Using  the  EMS  ranges  in  Table  2,  we  bound  the  EMS  pragmatically  between  the 
maximum and minimum EMS that could be practically received by the companies of 
which  bonds  would  be  offered  on  the  our  bond  protocol.  As  a  result,  the  Bond 
Spectrum  Model  directly  eliminates  any  bonds  from  issuers  that  fall  outside  these 
bounds.  
In  order  to  normalize  the  “notch” modification parameter used by Altman, we 
determine  the  number  of  notches  available  in  the  letter-grading  scheme  used  by 
him. The scheme has 22 notches between AAA and D. This means that each notch 
corresponds  to  a  change  of    points  in  our  normalized  EMS  score 
between  0100.  After  normalizing  the  EMS  and  integrating  our  additional  criteria, 
the result is rounded to the closest integer and matched to a color as follows: 
EMS
n
,
EMS
n
=
EMS
corporate
−EMS
min
EMS
max
−EMS
min
×100
EMS
min
=1.75andEMS
max
=8.15
100/22≊4.54
  of  2632

 
bondifinance.io
B. The Modification Criteria 
It  is  important  to  note  that  the  EMS  model  allows  analysts  to  further  adjust  the 
existing modification criteria as they see fit. However, we adhere to the limits set by 
Altman regarding the extent to which each criterion can impact the final EMS. 
2.ADJUST FOR FOREIGN CURRENCY DEVALUATION VULNERABILITY 
The  adjustment  according  to  this  modifier  is  made  by  assigning  a  high,  neutral,  or 
low currency devaluation vulnerability depending on: 
FX revenue / FX interest cost 
FX revenue / FX debt 
FX holdings / FX debt due next year 
Rate modification according to FX vulnerability is: 
High = 3 Notches 
Neutral = 1 Notch 
Low = No change 
Since each notch corresponds to 4.54 points in our numeric rating system between 
0100, this modifier may reduce the EMS between   and    
The firm’s industry is determined and the industry’s corresponding “Average Sector 
Credit Safety” rating is compared with the firm’s letter rating.   
3×4.541×4.54
  of  2732

 
bondifinance.io
  Table 3 
For every three notch difference between the firm’s rating and the sector rating, the 
firm’s   rating   is   adjusted   by   one   notch,   corresponding   to   4.54   points   in   our 
normalized EMS. 
≤ 3 notch difference:   One notch = 4.54 points  
3 to 6 notch difference:   Two notches = 4.54   2 points 
±
±
×
  of  2832

 
bondifinance.io
3. ADJUST FOR COMPETITIVE POSITION 
A corporate’s rating can be adjusted by a maximum of one notch (  4.54 points) in 
either direction according to the following parameters: 
•
Industry dominance 
•
Domestic power in terms of size  
•
Political influence 
•
Quality management 
4. ADJUST FOR SPECIAL DEBT ISSUE FEATURES 
Unique features of the issued bond are taken into consideration such has collateral 
or high-quality guarantors to further modify the rating. 
•
Senior Secured: 6.08 points 
•
Secured: 4.56 points 
•
Subordinated Secured: 3.04 points 
•
Senior Unsecured: 1.52 points 
•
Senior Preferred: 0 points 
•
Senior Non-Preferred: 1.52 points 
•
Senior Subordinated Unsecured: 3.04 points 
•
Subordinated Unsecured: 4.56 points 
•
Junior Subordinated Unsecured: 6.08 points 
5. ADJUST BY COMPARING TO US CORPORATE SPREAD AND SOVEREIGN SPREAD 
In the original EMS, this is actually proposed as an absolute parameter that decides 
if a corporate bond is worth investing or not. To calculate: 
a = US corporation of equal rating with the EM corporate   10 Year US Treasury 
b = EM corporate’s 10 Year sovereign bond   10 Year US Treasury 
±
−
−
  of  2932

 
bondifinance.io
 , then the bond is a good 
investment according to the EMS model. 
Instead, we propose a modifier: 
For each 1000 bps difference between EM corporate’s yield and (a + b + 10  Year US 
Treasury), modify the score by   1.52 points in the appropriate direction. 
Case for Emerging Market Corporate Bonds 
There  is  a  strong  case  to  make  for  emerging  market  corporate  bonds  based  on 
historical  evidence.  Since  the  year  2000,  emerging  market  corporate  bonds  have 
yielded higher returns compared to their U.S. counterparts. Moreover, these bonds 
have  exhibited  lower  default  rates  than  their  U.S.  counterparts  over  the  last  four 
decades. 
 1. Comparing Investment Grade Bonds 
Emerging   market   corporate   bonds   offer   higher   yields   compared   to   their 
counterparts in U.S. markets. Investment-grade emerging market corporate bonds, 
as  reported  by  the  ICE  BofA  High  Grade  Emerging  Markets  Corporate  Plus  Index, 
had an average yield of 4.86% between 2000 and 2024. In comparison, the  
average  yield  of  investment-grade  U.S.  corporate  bonds,  taken  from  5Ye a r   H i g h  
Quality  Market HQM  Corporate  Bond  data  provided  by  the  U.S.  Treasury,  and  the 
ICE  BofA  BBB  US  Corporate  Index,  was  4.41%  over  the  same  period.  The  average 
yield  on  “risk-free” 5Year  U.S.  Treasuries  during  this  time  was  2.71%  per  year. 
Consequently, investment-grade emerging market corporate bonds offered a  
If EM corporate's yield>(a+b+10YearUSTreasury)
±
  of  3032

 
bondifinance.io
10.20%  risk  premium  over  investment-grade  U.S.  corporate  bonds  and  a  79.34% 
premium over U.S. government debt. 
Between  1981  and  2023,  the  default  rate  for  investment-grade  emerging  market 
corporate  bonds  averaged  0.07%  annually  and  1.5%  over  a  cumulative  10-year 
period. In comparison, investment-grade U.S. corporate bonds had a default rate of 
0.11% annually and 2.37% over a cumulative 10-year period during the same period. 
This  indicates  that  the  default  risk  for  investment-grade  U.S.  corporates  over 
emerging market corporates has been on average 58% higher for a cumulative 10-
year period over the last four decades. Notably, there were no defaults in 2022 and 
2023 for investment-grade emerging market corporate bonds. 
27
2. Comparing High-Yield Bonds 
High-yield  emerging  market  bonds  provided  even  greater  returns  with  an  average 
yield of 9.46% over the same period, according to the ICE BofA High Yield Emerging 
Markets  Corporate  Plus  Index.  In  comparison,  high-yield  U.S.  corporate  bonds 
yielded  only  8.32%,  according  to  the  ICE  BofA  High  Yield  Index.  Thus,  high-yield 
emerging market bonds had a 13.70% risk premium over their U.S. counterparts and 
a 94.65% premium over investment-grade emerging market bonds. 
For  high-yield  emerging  market  corporate  bonds,  the  default  rate  averaged  2.58% 
annually and 12.7% over a cumulative 10-year period from 1981 to 2023. In contrast, 
high-yield U.S. corporates had a default rate of 3.95% annually and 22.22% over a 
cumulative  10-year  period  during  the  same  timeframe.  Therefore,  the  average 
default risk for a cumulative 10-year period for high-yield U.S. corporate bonds has 
been 74.96% higher than that for high-yield emerging market bonds over the last  
 https://www.spglobal.com/ratings/en/research/articles/240328-default-transition-and-recovery-2023-annual-global-
27
corporate-default-and-rating-transition-study-13047827
  of  3132

 
bondifinance.io
four  decades.  Additionally,  the  annual  default  rates  of  high-yield  emerging  market 
corporate  bonds  for  2022  and  2023  were  lower  than  the  average,  at  2.38%  and 
2.1% respectively. 
28
Despite offering higher yields, emerging market corporate bonds are also less risky 
than  their  U.S.  counterparts.  This  combination  of  higher  returns  and  lower  risk 
makes emerging market corporate bonds an attractive option for investors seeking 
better yields without significantly increasing their risk exposure. 
Conclusion 
Bondi Finance aims to open up a part of the financial world that’s often closed off to 
everyday  investors.  By  using  tokenization  and  a  clearer  way  of  measuring  credit 
quality,  we’re  making  emerging  market  corporate  bonds  easier  to  understand  and 
more   straightforward   to   access.   Instead   of   navigating   opaque   pricing,   high 
minimums,  and  limited  transparency,  investors  can  now  tap  into  opportunities  that 
offer higher yields and more global diversification. Both investment-grade and high-
yield segments have consistently delivered stronger returns, all while maintaining a 
lower  default  rate  over  an  extended  period  compared  to  US  counterparts.  Taken 
together,  these  factors  present  emerging  market  corporate  bonds  as  a  favorable 
opportunity for investors. 
Ultimately,  Bondi  Finance  is  part  of  a  larger  shift  toward  more  inclusive,  efficient 
markets.  By  lowering  barriers,  we  hope  to  channel  funds  toward  places  that  need 
them most, helping to foster growth and development in emerging economies. Over 
time,  we  believe  these  changes  can  bring  more  stability,  opportunity,  and  fairness 
to the bond market.
 https://www.spglobal.com/ratings/en/research/articles/240328-default-transition-and-recovery-2023-annual-global-
28
corporate-default-and-rating-transition-study-13047827 
  of  3232

## Metadata

- Pages: 32
- Version: 1.4
- Created: 2025-02-17T03:06:39.807Z
