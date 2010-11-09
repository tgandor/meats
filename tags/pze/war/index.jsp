<%@ page contentType="text/html; charset=UTF-8" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page isELIgnored="false" %>

<jsp:useBean class="pl.polsl.platforma.MainpageController" id="data" />

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<!-- The HTML 4.01 Transitional DOCTYPE declaration-->
<!-- above set at the top of the file will set     -->
<!-- the browser's rendering engine into           -->
<!-- "Quirks Mode". Replacing this declaration     -->
<!-- with a "Standards Mode" doctype is supported, -->
<!-- but may lead to some differences in layout.   -->


<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>PZE</title>
    <link href="style.css" type="text/css" rel="stylesheet" />
  </head>

  <body>
  
	<jsp:include page="login.jsp" />

    <h3>Linki do poszczególnych stron ocen</h3>
	
	<c:if test="${empty data.groups}" >
		<p class="warn">Brak grup do wyświetlenia.</p>
	</c:if>
	<c:if test="${empty data.tasks}" >
		<p class="warn">Brak zadań do wyświetlenia.</p>
	</c:if>
	
	<table>
		<tr>
			<td>&nbsp;</td>
			<c:forEach items="${data.groups}" var="group">
				<th>
					<a href="http://platforma.polsl.pl/rau2/grade/report/grader/index.php?id=51&group=${group.id}">${group.name}</a>	
					<c:if test="${data.userAdmin}">
						&nbsp;&nbsp;<a class="del" href="/pze/deleteGroup?key=${group.key.id}">&nbsp;X&nbsp;</a>      
					</c:if>
				</th>
		    </c:forEach>
		</tr>
	<c:forEach items="${data.tasks}" var="task">
		<tr>
			<th class="l">
				<c:if test="${data.userAdmin}">
					<a class="del" href="/pze/deleteTask?key=${task.key.id}">&nbsp;X&nbsp;</a>&nbsp;&nbsp;      
				</c:if>				
				<a href="http://platforma.polsl.pl/rau2/mod/assignment/view.php?id=${task.id}">${task.name}</a>
			</th>
			<c:forEach items="${data.groups}" var="group">
				<td class="mlink">
					<a href="http://platforma.polsl.pl/rau2/mod/assignment/submissions.php?id=${task.id}&group=${group.id}">lista</a>	      
				</td>
		    </c:forEach>			
		</tr>
	</c:forEach>
	
	</table>

	<c:if test="${data.userAdmin}">
	
	<div class="smallform">
		<p>Dodaj grupę:</p>
		<form action="/pze/addGroup">
			<table>
			<tr>
				<th>Nazwa:</th><td><input type="text" name="name" /></td>
			</tr>
			<tr>
				<th>Id:</th><td><input type="text" name="id" /></td>
			</tr>
			<tr>
				<td colspan="2" class="formend"><input type="submit" value="Dodaj" /></td>
			</tr>
			</table>
		</form>
	</div>

	<div class="smallform">
		<p>Dodaj zadanie:</p>
		<form action="/pze/addTask">
			<table>
			<tr>
				<th>Nazwa:</th><td><input type="text" name="name" /></td>
			</tr>
			<tr>
				<th>Id:</th><td><input type="text" name="id" /></td>
			</tr>
			<tr>
				<td colspan="2" class="formend"><input type="submit" value="Dodaj" /></td>
			</tr>
			</table>
		</form>
	</div>

	</c:if>
    
  </body>
</html>
