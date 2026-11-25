# Measuring the Textual Distinctiveness of German Book Prize Nominees against National Library Holdings

Code and analysis materials for a **submitted manuscript for the Digital Humanities conference 2027** comparing nominees of the German Book
Prize (*Deutscher Buchpreis*) against a near-complete control corpus of
contemporary German-language fiction. Includes the script for creating Table 1/Table 2 (`permutation_test.py`) as well as Figure 2 (`pca_plot.py`) in the paper. Both scripts expect two DataFrames (nominees and controls), where columns are calculated metrics and rows are individual works.

You can also access the `correlation_heatmap` of all metrics which informed our metric selection process.

This repository contains code, not the underlying book texts or full
metadata export. Metadata originates from the *Deutsche Nationalbibliothek* (DNB), corpus snapshot [DeLiKo-2026@DNB](https://doi.org/10.48694/kordaf.6183), state: 2026-06-22. You can still access the data through our virtual links:

[Nominees](https://korap.dnb.de/?q=%3Cbase%2Fs%3Dt%3E&cq=award+%3D+%22deutscher_buchpreis%22+%26+textSigle+%21%3D+%22DNB24%2FWIL%2F15156%22&ql=poliqarp)

[Control group](https://korap.dnb.de/?q=%3Cbase%2Fs%3Dt%3E&cq=translator+%21%3D+%2F.%2B%2F+%26+publisher+%3D+%2FZsolnay%2C+Paul%7CFISCHER+E-Books%7CeBook+Berlin+Verlag%7Cbtb+Verlag%7CLuchterhand+Literaturverlag%7CDeutscher+Taschenbuch+Verlag%7CD%C3%B6rlemann+Verlag+AG%7Cweissbooks%7CLenos+Verlag%7CVerlag+Das+Wunderhorn%7CVerbrecher+Verlag%7CHaymon+Verlag%7CCarl+Hanser+Verlag+GmbH+%26+Co.+KG%7CEichborn+digital%7CLeykam+Buchverlag%7CPalmArtPress%7CHanser%2C+Carl%7CResidenz+Verlag%7CKiepenheuer+%26+Witsch+eBook%7CD%C3%B6rlemann+eBook%7CSalis+Verlag%7CRowohlt+E-Book%7CSalzburg%7CC.+H.+Beck%7CBerenberg+Verlag+GmbH%7CUllstein+Ebooks%7CPicus+Verlag%7CDUMONT+Buchverlag%7CC.H.Beck%7CFischer+E-Books%7CSuhrkamp%7CKl%C3%B6pfer+%26+Meyer+Verlag%7CDiogenes+Verlag%7CDiogenes+Verlag+AG%7CE-Books+der+Verlagsgruppe+Random+House+GmbH%7CLiteraturverlag+Droschl%7CMatthes+%26+Seitz+Berlin+Verlag%7CWallstein+Verlag%7CKlett-Cotta%7CFolio+Verlag%7CHOFFMANN+UND+CAMPE+VERLAG+GmbH%7CRowohlt+Digitalbuch%7CJung+und+Jung%7CPaul+Zsolnay+Verlag%7CPenguin+Verlag%7CAufbau+Digital%7CBastei+Entertainment%7CUllstein+eBooks%7CVerlag+Antje+Kunstmann+GmbH%7CeBook+by+Kiepenheuer%26Witsch%7CSch%C3%B6ffling+%26+Co.%7CFrankfurter+Verlagsanstalt%7CPiper+ebooks%7CAlbrecht+Knaus+Verlag%7CKanon+Verlag%7CVerlag+Klaus+Wagenbach%7CDiaphanes%7COtto+M%C3%BCller+Verlag%7CSuhrkamp+Verlag%7CNagel+%26+Kimche%7CVoland+%26+Quist%7CJung+und+Jung+Verlag%2F+%26+award+%21%3D+%22deutscher_buchpreis%22&ql=poliqarp)

Note that "Lichtungen" by Iris Wolff was excluded from the nominee corpus for now, as the metric calculation pipeline erroneously produced NaNs for this work.
