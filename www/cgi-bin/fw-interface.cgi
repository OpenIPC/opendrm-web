#!/usr/bin/haserl --upload-limit=32 --upload-dir=/tmp
<%in p/common.cgi %>
<%
page_title="Interface Settings"

if [ "$REQUEST_METHOD" = "POST" ]; then
	case "$POST_action" in
		password)
			p1="$POST_password"
			p2="$POST_password_confirm"
			if [ -z "$p1" ]; then
				redirect_to "$SCRIPT_NAME" "danger" "Password cannot be empty."
			fi
			if [ "$p1" != "$p2" ]; then
				redirect_to "$SCRIPT_NAME" "danger" "Passwords do not match."
			fi
			echo "root:${p1}" | chpasswd
			touch /etc/shadow-
			redirect_back "success" "Password updated."
			;;
		theme)
			webui_theme="$POST_webui_theme"
			mkdir -p /etc/opendrm
			echo "webui_theme=\"${webui_theme}\"" > "$ui_config"
			redirect_back "success" "Theme updated."
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
			<h3>Access</h3>
			<form action="<%= $SCRIPT_NAME %>" method="post">
				<% field_hidden "action" "password" %>
				<div class="form-group">
					<label class="form-label" for="username">Username</label>
					<input type="text" id="username" name="username" value="root" disabled>
				</div>
				<% field_password "password" "New Password" %>
				<% field_password "password_confirm" "Confirm Password" %>
				<% button_submit "Change Password" %>
			</form>
		</div>
	</div>

	<div class="col">
		<div class="card">
			<h3>Appearance</h3>
			<form action="<%= $SCRIPT_NAME %>" method="post">
				<% field_hidden "action" "theme" %>
				<% field_select "webui_theme" "Theme" "${webui_theme:-dark}" "dark light" "Web interface color theme" %>
				<% button_submit "Apply Theme" %>
			</form>
		</div>
	</div>
</div>

<%in p/footer.cgi %>
