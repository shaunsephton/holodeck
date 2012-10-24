Changelog
=========

Next
----
#. Allowed for widget of-site embeds via phantomjs image generator `#8 <https://github.com/shaunsephton/holodeck/issues/8>`_.
#. Added dropdown to quickly change widget types (still need to ajaxify).
#. Switched to button groups, pretty.
#. Added tooltips buttons and metric titles, with metric title tooltip being metric description (new field added).
#. Limit export sheet names to 31 characters as imposed by Excel `#5 https://github.com/shaunsephton/holodeck/issues/5`_.

0.1.1 (2012-10-15)
------------------
#. Added mouse hover date formatter `#6 <https://github.com/shaunsephton/holodeck/issues/6>`_.
#. Widget groupings consistent on timestamp `#11 <https://github.com/shaunsephton/holodeck/issues/11>`_.
#. Samples are now unique on metric, string_value and timestamp, with existing sample integer_value fields being overriden on push `#13 <https://github.com/shaunsephton/holodeck/issues/13>`_.

0.1.0 (2012-08-25)
------------------
#. Added gage metric type `#7 <https://github.com/shaunsephton/holodeck/issues/7>`_.
#. Added drag and drop ordering of metrics on dashboard view `#9 <https://github.com/shaunsephton/holodeck/issues/9>`_.
#. Switched to Bootstrap scaffolding for metric/widget alignment/responsiveness `#10 <https://github.com/shaunsephton/holodeck/issues/10>`_.

0.0.9 (2012-08-16)
------------------
#. Prevented duplicate samples from breaking export (duplicates are ignored).
#. Prevented widgets from affecting each other through context copy.
#. Corrected broken footer links.

0.0.8 (2012-08-15)
------------------
#. Added Dashboard manage/edit view.
#. Allowed for purging of metric samples `#2 <https://github.com/shaunsephton/holodeck/issues/2>`_
#. Added public/sharing urls for dashboards `#4 <https://github.com/shaunsephton/holodeck/issues/4>`_

0.0.7 (2012-08-14)
------------------
#. Added Excel export action on Dashboard view.

0.0.6
-----
#. Switched to using `logan <https://github.com/dcramer/logan>`_

