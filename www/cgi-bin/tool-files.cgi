#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="File Browser"

# Restrict browsing to safe base directories
ALLOWED_BASE="/etc/opendrm /var/log /tmp/opendrm"
browse_path="${GET_path:-/etc/opendrm}"

# Canonicalize path and verify it starts with an allowed base
browse_path=$(realpath -m "$browse_path" 2>/dev/null || echo "/etc/opendrm")
safe=0
for base in $ALLOWED_BASE; do
	case "$browse_path" in
		"$base"|"$base"/*)
			safe=1
			break
			;;
	esac
done
[ "$safe" != "1" ] && browse_path="/etc/opendrm"
%>
<%in p/header.cgi %>

<div class="row">
	<div class="col-full">
		<div class="card">
			<h3>Files: <code><%= $browse_path %></code></h3>

			<% if [ -d "$browse_path" ]; then
				parent=$(dirname "$browse_path")
				echo "<table style=\"width:100%;border-collapse:collapse;font-size:0.85rem\">"
				echo "<thead><tr>"
				echo "<th style=\"text-align:left;padding:0.4rem;border-bottom:1px solid var(--border)\">Name</th>"
				echo "<th style=\"text-align:right;padding:0.4rem;border-bottom:1px solid var(--border)\">Size</th>"
				echo "<th style=\"text-align:left;padding:0.4rem;border-bottom:1px solid var(--border)\">Modified</th>"
				echo "</tr></thead><tbody>"
				if [ "$browse_path" != "/" ]; then
					echo "<tr><td style=\"padding:0.4rem\"><a href=\"?path=${parent}\">.. (parent)</a></td><td></td><td></td></tr>"
				fi
				ls -la "$browse_path" 2>/dev/null | tail -n +2 | while read -r perm _ _ _ size mon day time_yr name; do
					[ "$name" = "." ] || [ "$name" = ".." ] || [ -z "$name" ] && continue
					full="$browse_path/$name"
					if [ -d "$full" ]; then
						echo "<tr><td style=\"padding:0.4rem\"><a href=\"?path=${full}\">&#x1F4C1; ${name}/</a></td>"
					else
						echo "<tr><td style=\"padding:0.4rem\">&#x1F4C4; ${name}</td>"
					fi
					echo "<td style=\"padding:0.4rem;text-align:right\">${size}</td>"
					echo "<td style=\"padding:0.4rem\">${mon} ${day} ${time_yr}</td></tr>"
				done
				echo "</tbody></table>"
			elif [ -f "$browse_path" ]; then
				echo "<p class=\"small text-muted\">File: <code>${browse_path}</code></p>"
				echo "<pre>"
				cat "$browse_path" 2>/dev/null | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g"
				echo "</pre>"
				echo "<a href=\"?path=$(dirname "$browse_path")\" class=\"btn btn-secondary\">&larr; Back</a>"
			else
				echo "<p class=\"alert alert-warning\">Path not found: <code>${browse_path}</code></p>"
			fi %>
		</div>
	</div>
</div>

<%in p/footer.cgi %>
