#!/usr/bin/haserl
Content-type: text/html; charset=UTF-8
Cache-Control: no-store
Pragma: no-cache

<!DOCTYPE html>
<html lang="en" data-theme="<%= ${webui_theme:-dark} %>">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title><% html_title %></title>
	<link rel="stylesheet" href="/a/main.css">
	<script src="/a/main.js" defer></script>
</head>

<body id="page-<%= $pagename %>">
	<nav class="navbar">
		<a class="navbar-brand" href="/cgi-bin/status.cgi">
			<img alt="OpenDRM logo" height="28" src="/a/logo.svg">
		</a>

		<ul class="nav-links" id="nav-links">
			<li><a href="/cgi-bin/status.cgi"<% [ "$pagename" = "status" ] && echo ' class="active"' %>>Status</a></li>

			<li class="dropdown">
				<a>DRM ▾</a>
				<ul class="dropdown-menu">
					<li><a href="/cgi-bin/drm-settings.cgi">Settings</a></li>
					<li><a href="/cgi-bin/drm-license.cgi">License</a></li>
					<li class="dropdown-divider"></li>
					<li><a href="/cgi-bin/drm-streams.cgi">Streams</a></li>
				</ul>
			</li>

			<li class="dropdown">
				<a>Firmware ▾</a>
				<ul class="dropdown-menu">
					<li><a href="/cgi-bin/fw-network.cgi">Network</a></li>
					<li><a href="/cgi-bin/fw-interface.cgi">Interface</a></li>
					<li class="dropdown-divider"></li>
					<li><a href="/cgi-bin/fw-update.cgi">Update</a></li>
				</ul>
			</li>

			<li class="dropdown">
				<a>Tools ▾</a>
				<ul class="dropdown-menu">
					<li><a href="/cgi-bin/tool-console.cgi">Console</a></li>
					<li><a href="/cgi-bin/tool-files.cgi">Files</a></li>
				</ul>
			</li>
		</ul>
	</nav>

	<main>
		<div class="container">
			<div class="status-bar">
				<span class="sig x-small text-muted">
					<%= $(hostname -s 2>/dev/null || echo "opendrm") %> &mdash; OpenDRM
				</span>
				<span class="time x-small" id="time-now"></span>
			</div>

			<% log_read %>

			<div class="page-header">
				<h2><%= $page_title %></h2>
			</div>
