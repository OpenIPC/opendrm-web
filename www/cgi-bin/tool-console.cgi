#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Console"
%>
<%in p/header.cgi %>

<div class="row">
	<div class="col-full">
		<div class="card">
			<h3>Command Output</h3>
			<%
			if [ "$REQUEST_METHOD" = "POST" ] && [ -n "$POST_cmd" ]; then
				# Extract only the first word as the command and validate against allowlist
				cmd_word=$(echo "$POST_cmd" | awk '{print $1}')
				case "$cmd_word" in
					cat|ls|df|free|uptime|uname|hostname|ps|ip|ifconfig|netstat|\
					dmesg|logread|top|date|env|printenv|ping|traceroute|\
					opendrm|pidof|pgrep|grep|find|head|tail|wc|md5sum|sha256sum)
						echo "<div class=\"ex\"><h6># $POST_cmd</h6><pre>"
						$POST_cmd 2>&1 | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g"
						echo "</pre></div>"
						;;
					*)
						echo "<div class=\"alert alert-danger\">Command not allowed: <code>$(echo "$cmd_word" | sed 's/</\&lt;/g;s/>/\&gt;/g')</code></div>"
						;;
				esac
			fi
			%>
			<form action="<%= $SCRIPT_NAME %>" method="post">
				<div class="d-flex gap-2">
					<input type="text" name="cmd" id="cmd"
						value="<%= $(echo "$POST_cmd" | sed 's/"/\&quot;/g') %>"
						placeholder="Enter command..." autofocus style="flex:1">
					<input type="submit" class="btn btn-primary" value="Run">
				</div>
			</form>
		</div>
	</div>
</div>

<%in p/footer.cgi %>
