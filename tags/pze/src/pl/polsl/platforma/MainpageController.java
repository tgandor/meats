package pl.polsl.platforma;

import java.util.List;

import javax.jdo.PersistenceManager;
import javax.servlet.ServletRequest;

import com.google.appengine.api.users.UserService;
import com.google.appengine.api.users.UserServiceFactory;

import pl.polsl.platforma.model.Group;
import pl.polsl.platforma.model.PMF;
import pl.polsl.platforma.model.Task;

/**
 * Some bean for the mainpage. 
 * @author tomasz.gandor
 */
public class MainpageController {

	private UserService userService = UserServiceFactory.getUserService();
	private PersistenceManager pm = PMF.get().getPersistenceManager();

	public MainpageController() {		
	}
	
	@SuppressWarnings("unchecked")
	public List<Group> getGroups() {
		String query = "select from " + Group.class.getName() + " order by name";
		return (List<Group>) pm.newQuery(query).execute();
	}
	
	@SuppressWarnings("unchecked")
	public List<Task> getTasks() {
		String query = "select from " + Task.class.getName() + " order by name";
		return (List<Task>) pm.newQuery(query).execute();		
	}

	public boolean isLoggedIn() {
	    return userService.isUserLoggedIn();
	}
	
	public boolean isUserAdmin() {
		return isLoggedIn() && userService.isUserAdmin();
	}
	
	@Deprecated
	@SuppressWarnings("unchecked")
	public static void mainpageShow(ServletRequest req) {
		PersistenceManager pm = PMF.get().getPersistenceManager();
		String query = "select from " + Group.class.getName();
		List<Group> results = (List<Group>) pm.newQuery(query).execute();
		req.setAttribute("groups", results);
	}
}
