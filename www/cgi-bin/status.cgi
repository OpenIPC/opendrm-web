#!/usr/bin/haserl
<%in p/common.cgi %>

<% page_title="Device Status" %>
<%in p/header.cgi %>

<div class="row">
	<div class="col">
		<div class="card">
			<h3>Hardware</h3>
			<dl class="list small">
				<dt>Hostname</dt>
				<dd><%= $(hostname -s 2>/dev/null || echo "unknown") %></dd>
				<dt>Kernel</dt>
				<dd><%= $(uname -r 2>/dev/null || echo "unknown") %></dd>
				<dt>Architecture</dt>
				<dd><%= $(uname -m 2>/dev/null || echo "unknown") %></dd>
				<dt>Uptime</dt>
				<dd><%= $(uptime 2>/dev/null | sed 's/^ *//') %></dd>
			</dl>
		</div>
	</div>

	<div class="col">
		<div class="card">
			<h3>DRM Service</h3>
			<dl class="list small">
				<%
				drm_pid=$(pidof opendrm 2>/dev/null)
				if [ -n "$drm_pid" ]; then
					drm_status="<span class=\"badge badge-success\">Running</span>"
					drm_uptime=$(ps -o etime= -p "$drm_pid" 2>/dev/null | sed 's/ //g')
				else
					drm_status="<span class=\"badge badge-danger\">Stopped</span>"
					drm_uptime="—"
				fi
				%>
				<dt>Status</dt>
				<dd><%= $drm_status %></dd>
				<dt>PID</dt>
				<dd><%= ${drm_pid:-—} %></dd>
				<dt>Uptime</dt>
				<dd><%= $drm_uptime %></dd>
				<dt>Version</dt>
				<dd><%= $(opendrm --version 2>/dev/null || echo "unknown") %></dd>
			</dl>
		</div>
	</div>

	<div class="col">
		<div class="card">
			<h3>License</h3>
			<dl class="list small">
				<%
				if [ -n "$license_key" ]; then
					lic_status="<span class=\"badge badge-success\">Active</span>"
				else
					lic_status="<span class=\"badge badge-warning\">Not configured</span>"
				fi
				%>
				<dt>Status</dt>
				<dd><%= $lic_status %></dd>
				<dt>Key</dt>
				<dd><%= $([ -n "$license_key" ] && echo "${license_key%%-*}-****-****-****" || echo "—") %></dd>
				<dt>Expires</dt>
				<dd><%= ${license_expiry:-—} %></dd>
				<dt>Streams</dt>
				<dd><%= ${license_streams:-—} %></dd>
			</dl>
		</div>
	</div>
</div>

<div class="row">
	<div class="col">
		<div class="card">
			<h3>Resources</h3>
			<% ex "uptime" %>
			<% ex "df -h" %>
			<% ex "free -h" %>
		</div>
	</div>

	<div class="col">
		<div class="card">
			<h3>Network</h3>
			<%
			net_iface=$(ip route 2>/dev/null | awk '/default/ {print $5}' | head -n1)
			net_addr=$(ip route 2>/dev/null | grep "${net_iface:-eth0}" | awk '/src/ {print $7}' | head -n1)
			net_gw=$(ip route 2>/dev/null | awk '/default/ {print $3}' | head -n1)
			net_mac=$(cat /sys/class/net/${net_iface:-eth0}/address 2>/dev/null)
			%>
			<dl class="list small">
				<dt>Interface</dt>
				<dd><%= ${net_iface:-—} %></dd>
				<dt>IP Address</dt>
				<dd><%= ${net_addr:-—} %></dd>
				<dt>Gateway</dt>
				<dd><%= ${net_gw:-—} %></dd>
				<dt>MAC Address</dt>
				<dd><%= ${net_mac:-—} %></dd>
			</dl>
		</div>
	</div>
</div>

<%in p/footer.cgi %>
