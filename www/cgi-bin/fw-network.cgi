#!/usr/bin/haserl
<%in p/common.cgi %>
<%
page_title="Network Settings"

if [ "$REQUEST_METHOD" = "POST" ]; then
	case "$POST_action" in
		save)
			net_mode="${POST_net_mode:-dhcp}"
			net_address="$POST_net_address"
			net_mask="${POST_net_mask:-255.255.255.0}"
			net_gateway="$POST_net_gateway"
			net_dns="${POST_net_dns:-8.8.8.8}"
			net_hostname="$POST_net_hostname"

			if command -v setnetwork >/dev/null 2>&1; then
				setnetwork "$net_mode" "$net_address" "$net_mask" "$net_gateway" "$net_dns" "$net_hostname"
				redirect_back "success" "Network settings saved. Restart to apply."
			else
				redirect_to "$SCRIPT_NAME" "danger" "setnetwork utility not found."
			fi
			;;
		*)
			redirect_to "$SCRIPT_NAME" "danger" "Unknown action: $POST_action"
			;;
	esac
fi

# Read current network settings
net_iface=$(ip route 2>/dev/null | awk '/default/ {print $5}' | head -n1)
net_address=$(ip route 2>/dev/null | grep "${net_iface:-eth0}" | awk '/src/ {print $7}' | head -n1)
net_gateway=$(ip route 2>/dev/null | awk '/default/ {print $3}' | head -n1)
net_hostname=$(hostname -s 2>/dev/null)
net_dns=$(grep nameserver /etc/resolv.conf 2>/dev/null | head -n1 | awk '{print $2}')
%>
<%in p/header.cgi %>

<div class="row">
	<div class="col">
		<div class="card">
			<h3>Network Configuration</h3>
			<form action="<%= $SCRIPT_NAME %>" method="post">
				<% field_hidden "action" "save" %>
				<% field_select "net_mode" "Mode" "dhcp" "dhcp static" "Network addressing mode" %>
				<% field_string "net_hostname" "Hostname" "$net_hostname" "Device hostname" %>
				<% field_string "net_address" "IP Address" "$net_address" "Static IP address (used when mode is static)" %>
				<% field_string "net_mask" "Subnet Mask" "255.255.255.0" "Subnet mask" %>
				<% field_string "net_gateway" "Gateway" "$net_gateway" "Default gateway" %>
				<% field_string "net_dns" "DNS Server" "$net_dns" "Primary DNS server" %>
				<% button_submit %>
			</form>
		</div>
	</div>

	<div class="col">
		<div class="card">
			<h3>Current Status</h3>
			<% ex "ip addr show ${net_iface:-eth0} 2>/dev/null || echo 'Interface not found'" %>
			<% ex "ip route 2>/dev/null" %>
		</div>
	</div>
</div>

<%in p/footer.cgi %>
