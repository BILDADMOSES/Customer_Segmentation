import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;

@WebServlet("/HeaderServlet")
public class HeaderServlet extends HttpServlet {

    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // Get the "User-Agent" header
        String userAgent = request.getHeader("User-Agent");

        // Set the response content type
        response.setContentType("text/html");

        // Get the response writer
        PrintWriter out = response.getWriter();

        // Generate HTML response
        out.println("<html>");
        out.println("<head><title>Header Servlet Response</title></head>");
        out.println("<body>");
        out.println("<h1>User-Agent: " + userAgent + "</h1>");
        out.println("</body>");
        out.println("</html>");
    }
}
