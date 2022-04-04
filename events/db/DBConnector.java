package com.strato.db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import lombok.NonNull;




public class DBConnector{

   private static final Logger logger = LogManager.getLogger(DBConnector.class);
   private static final String JDBC_PREFIX = "jdbc:mysql://";

  /**
  * Creates a database connection via username + password authentication.
  *
  * @param username DB username
  * @param pwd DB password
  * @param dbEndpoint DB Instance (or proxy) endpoint
  * @return a Connection object
  */
  public static Connection createConnectionViaUserPwd( @NonNull String username,
                                                       @NonNull String pwd,
                                                       @NonNull String dbEndpoint) {
    Connection connection;

    try {
      logger.info ("Connecting to " + JDBC_PREFIX + dbEndpoint);
      connection = DriverManager.getConnection(JDBC_PREFIX + dbEndpoint, username, pwd);
      logger.info("Connection Established");
      return connection;

    } catch (SQLException e) {
      logger.info("Connection FAILED");
      logger.error(e.getMessage(), e);
    }

    return null;
  }

}
