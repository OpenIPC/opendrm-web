#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Firmware Update"

if [ "$REQUEST_METHOD" = "POST" ]; then
	case "$POST_action" in
		update)
			url="$POST_update_url"
			if [ -z "$url" ]; then
				redirect_to "$SCRIPT_NAME" "danger" "Update URL cannot be empty."
			fi
			# Validate URL format
			case "$url" in
				http://*|https://*)
					;;
				*)
					redirect_to "$SCRIPT_NAME" "danger" "Invalid URL. Must start with http:// or https://"
					;;
			esac
			# Download and apply firmware update
			tmpfile="/tmp/firmware_update.tar.gz"
			if wget -q -T30 -O "$tmpfile" "$url" 2>/dev/null; then
				if tar -tzf "$tmpfile" >/dev/null 2>&1; then
					# Schedule update after response is sent
					( sleep 2 && tar -xzf "$tmpfile" -C / 2>/dev/null && reboot ) &
					redirect_back "success" "Firmware downloaded. Device will restart to apply update."
				else
					rm -f "$tmpfile"
					redirect_to "$SCRIPT_NAME" "danger" "Downloaded file is not a valid firmware archive."
				fi
			else
				redirect_to "$SCRIPT_NAME" "danger" "Failed to download firmware from the provided URL."
			fi
			;;
		*)
			redirect_to "$SCRIPT_NAME" "danger" "Unknown action: $POST_action"
			;;
	esac
fi

current_version=$(cat /etc/openipc_version 2>/dev/null || echo "unknown")
%>
<%in p/header.cgi %>

<div class="row">
	<div class="col">
		<div class="card">
			<h3>Update Firmware</h3>
			<dl class="list small">
				<dt>Current Version</dt>
				<dd><%= $current_version %></dd>
			</dl>
			<form action="<%= $SCRIPT_NAME %>" method="post" class="mt-2">
				<% field_hidden "action" "update" %>
				<% field_string "update_url" "Firmware URL" "" "URL to the firmware image (.tar.gz)" %>
				<% button_submit "Start Update" "danger" %>
			</form>
			<div class="alert alert-warning mt-2">
				<strong>Warning:</strong> Do not power off the device during an update.
				An interrupted update may render the device unbootable.
			</div>
		</div>
	</div>

	<div class="col">
		<div class="card">
			<h3>System Info</h3>
			<% ex "cat /etc/os-release 2>/dev/null || echo 'Not available'" %>
		</div>
	</div>
</div>

<%in p/footer.cgi %>
