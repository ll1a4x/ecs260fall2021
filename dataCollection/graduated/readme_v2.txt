====================================================

Updated files:

files_changed_count_fetcher.py
fetch_dataset_features_graduated_projects.py

====================================================

Fixed 2 important bugs:

(1) 'NoneType' object has no attribute 'text'. 
This bug happend in "files_changed_count_fetcher.py" and added some checking conditions to make sure we don't collect None object's text. Skipping those should be fine since it's only affecting the variable "total_no_of_times_files_modified += files_modified"
The skipping won't significantly influence the validity of our project results.

(2) 404 error connecting to some github repo. 
Just skip those repos with invalid links. Those are very rare outliers.

Please see the comments in those 4 debugged sections to get more information.
====================================================

Note:
Re-collect the failed projects with errors (1) or (2) ONE BY ONE since those projects can be very huge.

If there is any other bug found later to cause incomplete collection of data, please show that in the group chat and let's fix them... (hopelly not found bugs anymore).

====================================================

- Lynden