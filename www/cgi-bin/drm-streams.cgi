#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Protected Streams"
streams_config=/etc/opendrm/streams.conf

if [ "$REQUEST_METHOD" = "POST" ]; then
	case "$POST_action" in
		add)
			stream_name="$POST_stream_name"
			stream_url="$POST_stream_url"
			stream_token="$POST_stream_token"
			if [ -z "$stream_name" ] || [ -z "$stream_url" ]; then
				redirect_to "$SCRIPT_NAME" "danger" "Stream name and URL are required."
			fi
			[ -z "$stream_token" ] && stream_token=$(head -c 16 /dev/urandom 2>/dev/null | od -An -tx1 | tr -d ' \n' || date +%s%N | sha256sum | head -c 32)
			mkdir -p /etc/opendrm
			echo "${stream_name}|${stream_url}|${stream_token}" >> "$streams_config"
			redirect_back "success" "Stream '${stream_name}' added."
			;;
		delete)
			stream_name="$POST_stream_name"
			# Escape special regex chars for safe sed use
			safe_name=$(printf '%s\n' "$stream_name" | sed 's/[[\.*^$()+?{}|]/\\&/g')
			if [ -f "$streams_config" ]; then
				sed -i "/^${safe_name}|/d" "$streams_config"
			fi
			redirect_back "success" "Stream '${stream_name}' removed."
			;;
		*)
			redirect_to "$SCRIPT_NAME" "danger" "Unknown action: $POST_action"
			;;
	esac
fi
%>
<%in p/header.cgi %>

<div class="row">
	<div class="col">
		<div class="card">
			<h3>Active Streams</h3>
			<%
			if [ -f "$streams_config" ] && [ -s "$streams_config" ]; then
				echo "<table style=\"width:100%;border-collapse:collapse;font-size:0.85rem\">"
				echo "<thead><tr>"
				echo "<th style=\"text-align:left;padding:0.4rem;border-bottom:1px solid var(--border)\">Name</th>"
				echo "<th style=\"text-align:left;padding:0.4rem;border-bottom:1px solid var(--border)\">Source URL</th>"
				echo "<th style=\"text-align:left;padding:0.4rem;border-bottom:1px solid var(--border)\">Token</th>"
				echo "<th style=\"padding:0.4rem;border-bottom:1px solid var(--border)\">Action</th>"
				echo "</tr></thead><tbody>"
				while IFS='|' read -r sname surl stoken; do
					[ -z "$sname" ] && continue
					echo "<tr>"
					echo "<td style=\"padding:0.4rem;border-bottom:1px solid var(--border)\">${sname}</td>"
					echo "<td style=\"padding:0.4rem;border-bottom:1px solid var(--border);word-break:break-all\"><code>${surl}</code></td>"
					echo "<td style=\"padding:0.4rem;border-bottom:1px solid var(--border)\"><code>${stoken:0:8}…</code></td>"
					echo "<td style=\"padding:0.4rem;border-bottom:1px solid var(--border);text-align:center\">"
					echo "<form action=\"$SCRIPT_NAME\" method=\"post\" style=\"display:inline\">"
					echo "<input type=\"hidden\" name=\"action\" value=\"delete\">"
					echo "<input type=\"hidden\" name=\"stream_name\" value=\"${sname}\">"
					echo "<input type=\"submit\" class=\"btn btn-danger\" value=\"Remove\""
					echo " onclick=\"return confirm('Remove stream ${sname}?')\">"
					echo "</form>"
					echo "</td></tr>"
				done < "$streams_config"
				echo "</tbody></table>"
			else
				echo "<p class=\"text-muted small\">No streams configured yet.</p>"
			fi
			%>
		</div>
	</div>

	<div class="col">
		<div class="card">
			<h3>Add Stream</h3>
			<form action="<%= $SCRIPT_NAME %>" method="post">
				<% field_hidden "action" "add" %>
				<% field_string "stream_name" "Stream Name" "" "Unique identifier (e.g. camera1)" %>
				<% field_string "stream_url" "Source URL" "" "RTSP or HTTP stream source (e.g. rtsp://127.0.0.1:554/stream=0)" %>
				<% field_string "stream_token" "Access Token" "" "Leave empty to auto-generate" %>
				<% button_submit "Add Stream" %>
			</form>
		</div>
	</div>
</div>

<%in p/footer.cgi %>
