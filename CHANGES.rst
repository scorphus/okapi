0.8.1 (unreleased)
------------------
- New Features:

  - Decouple okapi from requests so that any library following requests interface can be used

0.8.0 (2014-09-26)
------------------
- New features:

  - Use one collection per project instead of saving all projects in the same collection
  - Add a time_bucket attribute to make time based queries faster

0.7.1 (2014-07-28)
----------------
- Bug Fixes:

	-Make sure to raise the exception if an error occurs so the user know 
	exactly what is happening instead of code crashing
