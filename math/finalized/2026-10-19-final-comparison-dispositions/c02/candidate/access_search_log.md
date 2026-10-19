# Exact access and search log

Date: 2026-10-19. Window: approximately 00:05–00:07 UTC. Tool: web.run via functions orchestration. This log records requests and outcomes, not copyrighted theorem bodies. No primary paper body was recovered. Searches were bounded to these two named sources and their author/publisher routes; unrelated results were not pursued.

## Search batches, in order

1. Queries:
   - `Shibuya Sakaniwa 2001 generalized Hamming weights cyclic codes`
   - `Janwa Lal 1997 generalized Hamming weights`
   Outcome: identified IEICE title/date/pages; IEEE DOI and bibliographic/abstract leads; author-institution leads. Other generalized-weight papers were not used as substitutes.

2. Queries:
   - `"A Note on a Lower Bound for Generalized Hamming Weights" pdf`
   - `"On the generalized Hamming weights of cyclic codes" Janwa Lal pdf`
   - `"Shibuya" "Sakaniwa" "3138" pdf`
   - `"Janwa" "567719" pdf`
   Outcome: publisher abstract, bibliographies, Janwa author CV, IIT Kanpur annual publication list. No original body recovered.

3. Queries:
   - `site.iitk.ac.in "Lal" "generalized Hamming"`
   - `site.ramanujan.uprrp.edu "generalized" "cyclic"`
   - `site.shibuya.ei.sophia.ac.jp Hamming`
   - `"e84-a_12_3138" pdf`
   Outcome: no accessible target body. The speculative Shibuya institutional subdomain was a search term only, not a verified author site.

4. Queries:
   - `"Tomoharu Shibuya" publications`
   - `"Arbind" "Lal" homepage`
   - `"On the generalized Hamming weights of cyclic codes" filetype:pdf Janwa -site:sciencedirect.com -site:doi.org`
   Outcome: verified Shibuya Sophia profile; Lal institutional memorial record; bibliographic and CV leads.

5. Queries:
   - `"generalized Hamming" "Lal"`, domains: iitk.ac.in, uprrp.edu, hri.res.in
   - `"lower bound" "Hamming" "2001"`, domains: ts-lab.net, sophia.ac.jp, titech.ac.jp
   - `"A Note on a Lower Bound for Generalized Hamming Weights" theorem`
   - `"Janwa" "Lal" "Theorem" "1997" "cyclic"`
   Outcome: UPR bibliography, IIT Kanpur list, author CV indexed report number; a patent reference exposed historical author PDF path. The patent was a locator only, not theorem evidence.

6. Queries:
   - `"e84-a_12_3138.pdf"`
   - `"MRI-MATH/9/94"`
   - `"generalized Hamming" "Janwa" "pdf" "299"`
   - `"Shibuya" "Sakaniwa" "3138" "Theorem"`
   Outcome: publisher metadata and citations, report reference; no primary theorem body.

7. Final bounded queries:
   - `"567719"`, domain: ieeexplore.ieee.org
   - `"On the generalized Hamming weights of cyclic codes"`, domain: hri.res.in
   - `"A note on a lower bound" "Hamming"`, domains: titech.ac.jp, isct.ac.jp, ts-lab.net
   Outcome: no recovered target body. An unrelated current coding-theory page was not pursued.

## Direct opens and followed links

- https://globals.ieice.org/en_transactions/fundamentals/10.1587/e84-a_12_3138/_p
  Success: publisher abstract, bibliographic details, purchase/PDF control. No theorem text. Revisited via search references.
- https://doi.org/10.1109/18.567719
  Failure: URL inaccessible via tool.
- https://library.wolfram.com/infocenter/Articles/3134/
  Success: abstract/bibliography only; no paper download link in inspected page. Metadata author typo “Lai” noted.
- https://search.ieice.org/bin/summary.php?id=e84-a_12_3138
  Failure: internal error/inaccessible through tool.
- https://ieeexplore.ieee.org/document/567719
  Success only to a three-line JavaScript-required anti-robot interstitial. Reopened to verify this exact barrier. No article body.
- https://search.ieice.org/bin/keyword.php?category=A&kword=well-behaving&lang=E&year=2001
  Failure: internal error. Also tried the longer search-returned legacy URL with the `abst=j` plus URL-encoded backslash sequence; same inaccessible result. The search-index extract advertised a 271.2 KB full-text PDF, but no body was fetched.
- https://ramanujan.uprrp.edu/
  Success: author's university-hosted homepage; linked CV, not target paper.
- https://www.iitk.ac.in/math/index.php/faculty/faculty-profile/107
  Failure: internal error. This was an attempted institutional profile path, not evidence of identity/content.
- https://fst.sophia.ac.jp/en/faculty/tomoharu-shibuya
  Success: official author profile, links to laboratory and research database.
- https://www.ts-lab.net/
  Success via profile link: laboratory homepage; inspected navigation did not yield paper body.
- https://redb.cc.sophia.ac.jp/index.php?action=pages_view_main&active_action=cvclient_view_main_init&block_id=324&cvid=read0183734&display_type=cv&num=5&page=2&type=research_areas
  Followed from institutional profile; returned database landing page with an output-limit message, not paper text.
- https://ramanujan.uprrp.edu/cv-current-long-form.pdf
  Tried twice, first through author's homepage link and once directly. Both direct fetches returned `(400) Timeout fetching`; search index supplied bibliographic report locator only.
- https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=567719
  Failure: inaccessible via tool. Standard publisher full-text endpoint attempted; no authentication or paywall bypass.
- https://search.ieice.org/bin/pdf_link.php?category=A&lang=E&year=2001&fname=e84-a_12_3138&abst=
  Failure: inaccessible via tool. Legacy public PDF-link endpoint attempted; no paper fetched.
- https://www.ts-lab.net/members/tshibuya/pdf/e84-a_12_3138.pdf
  Failure: inaccessible via tool. Path located in a public citation at https://patents.justia.com/patent/8458474 . This locator is secondary; attempted file is author-hosted.
- http://www.ts-lab.net/members/tshibuya/pdf/e84-a_12_3138.pdf
  Redirected to HTTPS; same inaccessible outcome.
- https://www.iitk.ac.in/olddord/1996-97%20publication.pdf
  Success: 51-page institutional publication list. Find for `generalized Hamming` located printed p.129 / PDF index16, item7, with 43(1), 299–308. Only bibliographic evidence.
- https://www.ieice.org/publications/ken/article.php?day=20010316&expandable=0&ken_id=IT&lang=en&schedule_id=AA11370324_100%28696%29&society_cd=ESSNLS&year=2001
  Direct open failed; indexed publisher result supplied 16 March 2001 technical-report identifiers. No technical-report body recovered.

## Evidence boundary and stop

The exact query/open outcomes above exhaust this bounded pass. No contact with authors, purchases, sign-ins, CAPTCHA completion, broad related-literature expansion, or publication changes were performed. The barriers mean these tools/routes did not recover the originals; they do not establish that authorized library access or another lawful source cannot recover them. Bibliography/abstract records and later papers have not been promoted into the missing original theorem clauses.
