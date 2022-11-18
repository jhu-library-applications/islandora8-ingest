# islandora8-ingest

This repository helps you prepare CSVs for ingest via the [Migrate UI module](https://digital.library.jhu.edu/migrate_source_ui).

More documentation about metadata for Hopkins Digital Library (HDL) can be found at [Metadata Guide to Hopkins Digital Library](https://jhulibraries.atlassian.net/wiki/spaces/IDC/pages/1795883014/INFO+Metadata+guide+to+Hopkins+Digital+Library).
 
## addQuadsAndReplaceNamesInMetadataSheet.py
This script adds the correct quad look-up prefix to taxonoomy terms, and replaces term names with their unique_identifiers. See comments in script for more details.

## combineContributorsAddRelatorPrefixes
This script combines columns named by relator terms into a contributor column and adds relator prefixes to the beginning of the name or unique identifiers.

## createFindAndReplaceSheets.py

## findNewTaxonomyTerms.py
This script compares "uniqueTaxonomyTermsFromMetadataSheet.csv" and "allExistingTaxonomies.csv" to find what taxonomy terms in your metadata sheet need to be added to HDL.

## findReplaceInSheet.py
This script uses a spreadsheet with columns 'to_delete' and 'to_keep' to replace taxonomy terms found in specified columns in your metadata spreadsheet. (Adjust columns searched by adding or removing column names in the columnsToSearch list.)

## generateUUIDs.py
This script adds a UUID identifier for each row in all CSV spreadsheets in a specified directory.

## getIslandora8RepositoryItems.py

## getIslandora8TaxonomyTerms.py
This script gets all taxonomy terms from HDL and generates spreadsheets for each, as well as a spreadsheet call "allExistingTaxonomies.csv" that contains all terms.

## get UniqueListsOfTaxonomyTermsFromMetadataSheet.csv
This script generates a spreadsheet, "uniqueTaxonomyTermsFromMetadataSheet.csv" containing all unique taxonomy terms from your metadata spreadsheet. Adjust taxonomyColumns variable to control what columns it grabs terms from.