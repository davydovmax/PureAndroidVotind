%#template to generate a HTML list from a list of strings)
<p>Server logs:</p>
<ul border="1">
%for row in rows:
    <li>{{row}}</li>
%end
</ul>