#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="DRM License"
license_config=/etc/opendrm/license.conf

if [ "$REQUEST_METHOD" = "POST" ]; then
	case "$POST_action" in
		activate)
			key="$POST_license_key"
			if [ -z "$key" ]; then
				redirect_to "$SCRIPT_NAME" "danger" "License key cannot be empty."
			fi
			mkdir -p /etc/opendrm
			cat > "$license_config" <<EOF
license_key="${key}"
license_expiry=""
license_streams=""
EOF
			# Attempt online activation if network is available (key passed via POST body)
			if [ -n "$(ip route | awk '/default/ {print $3}')" ]; then
				result=$(wget -q -T5 -O- \
					--post-data="key=${key}&host=$(hostname -s)" \
					"https://license.openipc.org/activate" \
					2>/dev/null)
				if [ -n "$result" ]; then
					expiry=$(echo "$result" | grep -o '"expiry":"[^"]*"' | cut -d'"' -f4)
					streams=$(echo "$result" | grep -o '"streams":[0-9]*' | cut -d':' -f2)
					[ -n "$expiry" ]  && sed -i "s/license_expiry=\"\"/license_expiry=\"${expiry}\"/" "$license_config"
					[ -n "$streams" ] && sed -i "s/license_streams=\"\"/license_streams=\"${streams}\"/" "$license_config"
					redirect_back "success" "License activated successfully."
				fi
			fi
			redirect_back "success" "License key saved (offline mode)."
			;;
		remove)
			rm -f "$license_config"
			redirect_back "success" "License removed."
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
			<h3>License Key</h3>
			<%
			if [ -n "$license_key" ]; then
			%>
			<dl class="list small">
				<dt>Key</dt>
				<dd><code><%= $license_key %></code></dd>
				<dt>Expires</dt>
				<dd><%= ${license_expiry:-Not available} %></dd>
				<dt>Max Streams</dt>
				<dd><%= ${license_streams:-Not available} %></dd>
			</dl>
			<form action="<%= $SCRIPT_NAME %>" method="post" class="mt-2">
				<% field_hidden "action" "remove" %>
				<input type="submit" class="btn btn-danger" value="Remove License"
					onclick="return confirm('Remove the current license?')">
			</form>
			<% else %>
			<p class="text-muted small">No license configured. Enter your license key below.</p>
			<form action="<%= $SCRIPT_NAME %>" method="post">
				<% field_hidden "action" "activate" %>
				<% field_string "license_key" "License Key" "" "Your OpenDRM license key (format: XXXX-XXXX-XXXX-XXXX)" %>
				<% button_submit "Activate" %>
			</form>
			<% fi %>
		</div>
	</div>

	<div class="col">
		<div class="card">
			<h3>About Licensing</h3>
			<p class="small text-muted">
				OpenDRM requires a valid license key to enable stream protection features.
				Free evaluation licenses are available for testing purposes.
			</p>
			<p class="small text-muted">
				To obtain a license key, please visit
				<a href="https://openipc.org/">openipc.org</a> or contact
				<a href="mailto:dev@openipc.org">dev@openipc.org</a>.
			</p>
			<p class="small text-muted">
				License activation requires an active internet connection.
				Offline activation is available for air-gapped deployments.
			</p>
		</div>
	</div>
</div>

<%in p/footer.cgi %>
