<%@ page import="com.google.appengine.api.users.User" %>
<%@ page import="com.google.appengine.api.users.UserService" %>
<%@ page import="com.google.appengine.api.users.UserServiceFactory" %>

<div style="text-align: right;">
	<%
	    UserService userService = UserServiceFactory.getUserService();
	    User user = userService.getCurrentUser();
	    if (user != null) {
	%>
	<p>Witamy, <%= user.getNickname() %>! 
		<a href="<%= userService.createLogoutURL(request.getRequestURI()) %>">Wyloguj</a>
	</p>
	<%
	    } else {
	%>
	<p>Hello!
		<a href="<%= userService.createLoginURL(request.getRequestURI()) %>">Zaloguj</a>
	</p>
	<%
	    }
	%>
</div>