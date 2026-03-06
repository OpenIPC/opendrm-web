#!/usr/bin/haserl
<%
IFS_ORIG=$IFS

# tag "tag" "text" "css" "extras"
tag() {
	local t="$1"
	local n="$2"
	local c="$3"
	[ -n "$c" ] && c=" class=\"${c}\""
	local x="$4"
	[ -n "$x" ] && x=" ${x}"
	echo "<${t}${c}${x}>${n}</${t}>"
}

# alert "text" "type"
alert() {
	echo "<div class=\"alert alert-${2:-info}\">${1}</div>"
}

# button_submit "text" "type"
button_submit() {
	local t="${1:-Save Changes}"
	local c="${2:-primary}"
	echo "<div class=\"mt-2\"><input type=\"submit\" class=\"btn btn-${c}\" value=\"${t}\"></div>"
}

# field_hidden "name" "value"
field_hidden() {
	echo "<input type=\"hidden\" name=\"${1}\" id=\"${1}\" value=\"${2}\">"
}

# field_string "name" "label" "value" "hint"
field_string() {
	local n="$1"
	local l="$2"
	local v="$3"
	local h="$4"
	[ "$v" = "eval" ] && v=$(t_value "$n")
	echo "<div class=\"form-group\">"
	echo "<label class=\"form-label\" for=\"${n}\">${l}</label>"
	echo "<input type=\"text\" id=\"${n}\" name=\"${n}\" class=\"form-control\" value=\"${v}\">"
	[ -n "$h" ] && echo "<small class=\"text-muted\">${h}</small>"
	echo "</div>"
}

# field_password "name" "label" "hint"
field_password() {
	local n="$1"
	local l="$2"
	local h="$3"
	echo "<div class=\"form-group\">"
	echo "<label class=\"form-label\" for=\"${n}\">${l}</label>"
	echo "<div class=\"d-flex gap-2\">"
	echo "<input type=\"password\" id=\"${n}\" name=\"${n}\" class=\"form-control\" value=\"\">"
	echo "<label class=\"form-check\" style=\"white-space:nowrap\">"
	echo "<input type=\"checkbox\" data-for=\"${n}\"> show"
	echo "</label>"
	echo "</div>"
	[ -n "$h" ] && echo "<small class=\"text-muted\">${h}</small>"
	echo "</div>"
}

# field_select "name" "label" "value" "options" "hint"
field_select() {
	local n="$1"
	local l="$2"
	local v="$3"
	local opts="$4"
	local h="$5"
	[ "$v" = "eval" ] && v=$(t_value "$n")
	echo "<div class=\"form-group\">"
	echo "<label class=\"form-label\" for=\"${n}\">${l}</label>"
	echo "<select id=\"${n}\" name=\"${n}\">"
	for o in $opts; do
		if [ "$v" = "$o" ]; then
			echo "<option value=\"${o}\" selected>${o}</option>"
		else
			echo "<option value=\"${o}\">${o}</option>"
		fi
	done
	echo "</select>"
	[ -n "$h" ] && echo "<small class=\"text-muted\">${h}</small>"
	echo "</div>"
}

# field_switch "name" "label" "value" "hint"
field_switch() {
	local n="$1"
	local l="$2"
	local v="$3"
	local h="$4"
	[ "$v" = "eval" ] && v=$(t_value "$n")
	[ "$v" = "true" ] && local chk="checked" || local chk=""
	echo "<div class=\"form-group\">"
	echo "<div class=\"form-check\">"
	echo "<input type=\"hidden\" name=\"${n}\" value=\"false\">"
	echo "<input type=\"checkbox\" id=\"${n}\" name=\"${n}\" value=\"true\" ${chk}>"
	echo "<label for=\"${n}\" class=\"form-label\" style=\"display:inline;margin:0\">${l}</label>"
	echo "</div>"
	[ -n "$h" ] && echo "<small class=\"text-muted\">${h}</small>"
	echo "</div>"
}

# field_integer "name" "label" "value" "min" "max" "hint"
field_integer() {
	local n="$1"
	local l="$2"
	local v="$3"
	local x="$4"
	local y="$5"
	local h="$6"
	echo "<div class=\"form-group\">"
	echo "<label class=\"form-label\" for=\"${n}\">${l}</label>"
	echo "<input type=\"number\" id=\"${n}\" name=\"${n}\" value=\"${v}\" min=\"${x}\" max=\"${y}\" step=\"1\">"
	[ -n "$h" ] && echo "<small class=\"text-muted\">${h}</small>"
	echo "</div>"
}

# field_textarea "name" "label" "value" "hint"
field_textarea() {
	local n="$1"
	local l="$2"
	local v="$3"
	local h="$4"
	echo "<div class=\"form-group\">"
	echo "<label class=\"form-label\" for=\"${n}\">${l}</label>"
	echo "<textarea id=\"${n}\" name=\"${n}\" rows=\"6\" style=\"font-family:monospace\">${v}</textarea>"
	[ -n "$h" ] && echo "<small class=\"text-muted\">${h}</small>"
	echo "</div>"
}

# ex "command"
ex() {
	echo "<div class=\"ex\"><h6># ${1}</h6><pre>"
	eval "$1" | sed "s/&/\&amp;/g;s/</\&lt;/g;s/>/\&gt;/g;s/\"/\&quot;/g"
	echo "</pre></div>"
}

check_password() {
	local p="/cgi-bin/fw-interface.cgi"
	[ -z "$SCRIPT_NAME" ] || [ "$SCRIPT_NAME" = "${p}" ] && return
	# /etc/shadow- is created by fw-interface.cgi as a sentinel after the
	# user has set a custom password (same pattern as majestic-webui).
	# Also verify the root password hash is non-empty in /etc/shadow.
	local shadow_hash
	shadow_hash=$(grep "^root:" /etc/shadow 2>/dev/null | cut -d: -f2)
	if [ ! -f /etc/shadow- ] || [ -z "$shadow_hash" ]; then
		redirect_to "${p}" "danger" "You must set your own secure password!"
	fi
}

log_file=/tmp/opendrm/logfile.txt

log_create() {
	echo "${1}:${2}" > "$log_file"
}

log_read() {
	[ ! -f "$log_file" ] && return
	[ -z "$(cat "$log_file")" ] && return
	local c m l
	OIFS="$IFS"
	IFS=$'\n'
	for l in $(cat "$log_file"); do
		c="$(echo "$l" | cut -d':' -f1)"
		m="$(echo "$l" | cut -d':' -f2-)"
		echo "<div class=\"alert alert-${c}\" data-autohide>${m}</div>"
	done
	IFS="$OIFS"
	rm -f "$log_file"
}

# redirect_to "url" "flash class" "flash text"
redirect_to() {
	[ -n "$3" ] && log_create "$2" "$3"
	echo "HTTP/1.1 303 See Other"
	echo "Content-type: text/html; charset=UTF-8"
	echo "Cache-Control: no-store"
	echo "Pragma: no-cache"
	echo "Location: $1"
	echo
	exit 0
}

# redirect_back "flash class" "flash text"
redirect_back() {
	redirect_to "${HTTP_REFERER:-/}" "$1" "$2"
}

t_value() {
	eval "echo \$${1}"
}

html_title() {
	[ -n "$page_title" ] && echo -n "$page_title"
	echo -n " - OpenDRM"
}

include() {
	[ -f "$1" ] && . "$1"
}

drm_config=/etc/opendrm/opendrm.conf
ui_config=/etc/opendrm/webui.conf

[ ! -d /etc/opendrm ]    && mkdir -p /etc/opendrm
[ ! -d /tmp/opendrm ]    && mkdir -p /tmp/opendrm

include "$drm_config"
include "$ui_config"
include /etc/opendrm/license.conf

pagename=$(basename "$SCRIPT_NAME")
pagename="${pagename%%.*}"

check_password
%>
