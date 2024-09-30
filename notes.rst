
Documentation Workflow Overview
===============================

1. Exclude Autosummary Directory in `.gitignore`
------------------------------------------------
If you've modified the hierarchy in the API reference documentation, make sure to add the new `autosummary` directory to the `.gitignore`. These builds are not meant to be pushed to the repository. They should only be generated during the Read the Docs (RTD) build process.

2. Customizing Colors and Table Widths with CSS
-----------------------------------------------
Any changes to the colors of bars, table widths, or similar elements should be done through the `custom.css` file. This file is referenced in `conf.py`, so any modifications will be directly applied to the theme.

3. PyData Sphinx Theme Resources
--------------------------------
We are using the PyData Sphinx theme, which is well-documented and widely used by projects like NumPy and Matplotlib. You can refer to their repositories on GitHub and review their `conf.py` and `index.rst` files if you want to implement similar configurations.

4. Cross-Referencing in RST
---------------------------
To cross-reference within an RST file, you need to first name the section you want to reference. For example, the API reference page might start with::

    .. _api:

You can reference this section using::

    :ref:`Description text <api>`

Similarly, for a section named `.. _measurement_modules`, you can reference it as::

    :ref:`Description text <measurement_modules>`

5. Structuring Index Files with Toctree
---------------------------------------
The best approach to creating index files with subdirectories is to create an index file for the parent, then use a `toctree` directive to call the child index files. Continue this until you reach the last directory. Afterward, manually list the modules. We had to do this due to the removal of the `__init__.py` file, which Sphinx uses to detect modules and ensure a complete hierarchy.

6. Rendering First RST Page in a Directory
------------------------------------------
To render the first RST page in a directory automatically, use the `include` directive like so::

    .. _api:

    API Reference
    =============

    .. toctree::
        :maxdepth: 6
        :hidden:

        ../core/index
        ../gui/index 
        ../logic/index 
        ../tasks/index
        ../tools/index
        ../util/index

    .. include:: ../core/index.rst

Ensure that the parent `toctree` is hidden to avoid displaying the entire tree structure.

7. Recursive Toctree for Methods and Functions
----------------------------------------------
For the final level in the `toctree`, use the `:recursive:` keyword to include all functions and methods inside the modules and classes.

8. 404 Error Links
------------------
Some links may currently lead to 404 errors because the pages they reference are not yet documented. These links will be updated as documentation is added, using the cross-referencing method mentioned above.

9. Custom Module Template Issues
--------------------------------
The custom module template gathers all classes, methods, attributes, and functions, but a problem arises when the module page lists deprecated documentation. Clicking on the items in the table still leads to the correct class documentation, but further investigation into the template is needed to resolve this duplication.

10. Conf.py Dependencies and Themes
-----------------------------------
In the `conf.py` file, include only the dependencies you're actively using. Multiple themes can cause conflicts. For example, we encountered a rendering issue caused by having both the Sphinx Book Theme and PyData Sphinx Theme listed, even though we were only using the PyData Sphinx Theme.

11. Modifying the PyData Sphinx Theme
-------------------------------------
Modifications to the PyData Sphinx theme, such as the logo, project title, top bar, and sidebar visibility, are handled in the `conf.py` under the `html_theme_options` section. For instance, if the left sidebar disappears on some pages, it could be due to incorrect `nav_level` depth settings.

12. Disabling Show Inheritance
------------------------------
Always disable the `show_inheritance` option, as it unnecessarily renders inherited methods from external libraries (e.g., PySide), which significantly increases the build time.

13. Cross-Referencing Between RTD Projects
------------------------------------------
To cross-reference two different Read the Docs (RTD) projects (e.g., iqo-modules and quid-core), you need to include references in the `conf.py` file for each project as follows::

    intersphinx_mapping = {
        'iqo': ('https://qudi-iqo-modules.readthedocs.io/en/george/index.html', None),
    }

You can then reference, for example, the installation section of `iqo` as::

    :ref:`description <iqo:installation>`

if `installation.rst` has this tag reference at the beginning::

    .. _installation:

14. Creating a Custom Landing Page
----------------------------------
You can create a custom landing page by adding grids or any text in the `index.rst` file. This will render on your project's home page. Refer to other projects using the PyData Sphinx theme for inspiration.

15. Optimizing Makefile for Build Time
--------------------------------------
We have modified the `Makefile` to rebuild only the parts of the project that have changed, significantly reducing build times during local development.

16. License in RST Files
------------------------
To include the license in every RST file without rendering it, simply comment it out with `..` at the beginning of the line.

17. Converting Documentation to NumPy Style
-------------------------------------------
There are online tools for converting documentation to NumPy style, but we found they were not accurate. While using ChatGPT has been a better alternative, it doesn't work well for large files. However, it's still much faster than manual conversion.

18. Documentation Coverage and Error Tracking
---------------------------------------------
Two new files have been added to track documentation coverage: `calculate_documentation_coverage` computes the percentage of undocumented methods or classes, while `count_python_errors` tracks Python errors by file, useful for statistical analysis of the documentation.

19. Dependency Management in `pyproject.toml`
--------------------------------------------
Ensure that every dependency and its correct version is listed in the `pyproject.toml` file to guarantee a successful build on RTD.
