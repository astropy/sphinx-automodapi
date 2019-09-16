{{ objname }}
{{ underline }}


.. currentmodule:: {{ module }}


{% if objtype in ['class'] %}
.. auto{{ objtype }}:: {{ objname }}
    :show-inheritance:

{% else %}
.. auto{{ objtype }}:: {{ objname }}

{% endif %}

{% if objtype in ['class', 'method', 'function'] %}
.. raw:: html

    <div class="clearer"></div>

{% endif %}
