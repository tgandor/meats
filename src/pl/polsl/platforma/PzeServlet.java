package pl.polsl.platforma;

import java.io.IOException;

import javax.jdo.PersistenceManager;
import javax.servlet.http.*;

import pl.polsl.platforma.model.Group;
import pl.polsl.platforma.model.PMF;
import pl.polsl.platforma.model.Task;

@SuppressWarnings("serial")
public class PzeServlet extends HttpServlet {
		
	public void addGroup(HttpServletRequest req) {
		String id = req.getParameter("id");
		String name = req.getParameter("name");
		if ( id != null && name != null) {
			Group g = new Group(id, name);
			PersistenceManager pm = PMF.get().getPersistenceManager();
			try {
				pm.makePersistent(g);
			} finally {
				pm.close();
			}
		}
	}

	public void addTask(HttpServletRequest req) {
		String id = req.getParameter("id");
		String name = req.getParameter("name");
		if ( id != null && name != null) {
			Task g = new Task(id, name);
			PersistenceManager pm = PMF.get().getPersistenceManager();
			try {
				pm.makePersistent(g);
			} finally {
				pm.close();
			}
		}
	}
	
	public void deleteGroup(HttpServletRequest req) {
		String keyStr = req.getParameter("key");
		if ( keyStr != null ) {
			PersistenceManager pm = PMF.get().getPersistenceManager();
			try {
				long key = Long.parseLong(keyStr);
				Group g = (Group) pm.getObjectById(Group.class, key);
				pm.deletePersistent(g);
			} finally {
				pm.close();
			}
		}
	}
	
	public void deleteTask(HttpServletRequest req) {
		String keyStr = req.getParameter("key");
		if ( keyStr != null ) {
			PersistenceManager pm = PMF.get().getPersistenceManager();
			try {
				long key = Long.parseLong(keyStr);
				Task g = (Task) pm.getObjectById(Task.class, key);
				pm.deletePersistent(g);
			} finally {
				pm.close();
			}
		}
	}
	
	@Override
	public void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws IOException {
		String action = req.getRequestURI().replace("/pze/", "");
		try {
			getClass().getMethod(
					action, 
					new Class<?>[]{HttpServletRequest.class}
				).invoke(this, req);
			resp.sendRedirect("/");
		} catch (Exception e) {
			e.printStackTrace(resp.getWriter());
			resp.getWriter().println("Error encountered");
		}
	}
	
}
