#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="DRM Settings"

if [ "$REQUEST_METHOD" = "POST" ]; then
	case "$POST_action" in
		save)
			drm_enabled="$POST_drm_enabled"
			drm_port="${POST_drm_port:-8090}"
			drm_bind="${POST_drm_bind:-0.0.0.0}"
			drm_log_level="${POST_drm_log_level:-info}"
			drm_max_streams="${POST_drm_max_streams:-4}"

			mkdir -p /etc/opendrm
			cat > "$drm_config" <<EOF
drm_enabled="${drm_enabled}"
drm_port="${drm_port}"
drm_bind="${drm_bind}"
drm_log_level="${drm_log_level}"
drm_max_streams="${drm_max_streams}"
EOF
			redirect_back "success" "DRM settings saved."
			;;
		restart)
			/etc/init.d/opendrm restart >/dev/null 2>&1 || \
				killall opendrm 2>/dev/null; opendrm &
			redirect_back "success" "DRM service restarted."
			;;
		stop)
			/etc/init.d/opendrm stop >/dev/null 2>&1 || killall opendrm 2>/dev/null
			redirect_back "success" "DRM service stopped."
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
			<h3>General</h3>
			<form action="<%= $SCRIPT_NAME %>" method="post">
				<% field_hidden "action" "save" %>
				<% field_switch "drm_enabled" "Enable DRM Service" "${drm_enabled:-true}" "Start the OpenDRM service on boot" %>
				<% field_string "drm_bind" "Bind Address" "${drm_bind:-0.0.0.0}" "IP address to listen on (0.0.0.0 for all interfaces)" %>
				<% field_integer "drm_port" "Port" "${drm_port:-8090}" "1024" "65535" "TCP port for the DRM service" %>
				<% field_integer "drm_max_streams" "Max Streams" "${drm_max_streams:-4}" "1" "64" "Maximum number of concurrent protected streams" %>
				<% field_select "drm_log_level" "Log Level" "${drm_log_level:-info}" "debug info warning error" "Verbosity of the DRM service log" %>
				<% button_submit %>
			</form>
		</div>
	</div>

	<div class="col">
		<div class="card">
			<h3>Service Control</h3>
			<p class="text-muted small">Manage the OpenDRM service state.</p>
			<div class="d-flex gap-2 mt-2">
				<form action="<%= $SCRIPT_NAME %>" method="post">
					<% field_hidden "action" "restart" %>
					<input type="submit" class="btn btn-primary" value="Restart">
				</form>
				<form action="<%= $SCRIPT_NAME %>" method="post">
					<% field_hidden "action" "stop" %>
					<input type="submit" class="btn btn-danger" value="Stop"
						onclick="return confirm('Stop the DRM service?')">
				</form>
			</div>
		</div>

		<div class="card mt-2">
			<h3>Service Log</h3>
			<% ex "tail -n 20 /var/log/opendrm.log 2>/dev/null || echo 'No log available'" %>
		</div>
	</div>
</div>

<%in p/footer.cgi %>
