import org.apache.log4j.{Level, Logger}
import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

object ManageTrajectory {

  Logger.getLogger("org.spark_project").setLevel(Level.WARN)
  Logger.getLogger("org.apache").setLevel(Level.WARN)
  Logger.getLogger("akka").setLevel(Level.WARN)
  Logger.getLogger("com").setLevel(Level.WARN)

  def loadTrajectoryData(spark: SparkSession, filePath: String): DataFrame = {

    val df = spark.read.option("multiline", "true").json(filePath)
    val df2 = df.select(
      col("trajectory_id"),
      col("vehicle_id"),
      explode(col("trajectory")) as "trajectory"
    )

    df2
  }

  def getSpatialRange(
      spark: SparkSession,
      dfTrajectory: DataFrame,
      latMin: Double,
      lonMin: Double,
      latMax: Double,
      lonMax: Double
  ): DataFrame = {
    import spark.implicits._

    var tempVehDF = dfTrajectory.filter(
      dfTrajectory("trajectory.location").getItem(
        0
      ) >= latMin and dfTrajectory(
        "trajectory.location"
      ).getItem(0) <= latMax and dfTrajectory("trajectory.location")
        .getItem(1) >= lonMin and dfTrajectory(
        "trajectory.location"
      ).getItem(1) <= lonMax
    )

    tempVehDF = tempVehDF
      .groupBy("trajectory_id", "vehicle_id")
      .agg(collect_list("trajectory") as "trajectory")

    val spatialRangeVehicleDF = tempVehDF.select(
      $"trajectory_id",
      $"vehicle_id",
      $"trajectory.timestamp" as "timestamp",
      $"trajectory.location" as "location"
    )

    spatialRangeVehicleDF
  }

  def getSpatioTemporalRange(
      spark: SparkSession,
      dfTrajectory: DataFrame,
      timeMin: Long,
      timeMax: Long,
      latMin: Double,
      lonMin: Double,
      latMax: Double,
      lonMax: Double
  ): DataFrame = {
    /* TO DO */
    import spark.implicits._

    var tempVehDF = dfTrajectory.filter(
      dfTrajectory("trajectory.location").getItem(
        0
      ) >= latMin and dfTrajectory(
        "trajectory.location"
      ).getItem(0) <= latMax and dfTrajectory("trajectory.location")
        .getItem(1) >= lonMin and dfTrajectory(
        "trajectory.location"
      ).getItem(1) <= lonMax and dfTrajectory(
        "trajectory.timestamp"
      ) >= timeMin and dfTrajectory("trajectory.timestamp") <= timeMax
    )

    tempVehDF = tempVehDF
      .groupBy("trajectory_id", "vehicle_id")
      .agg(collect_list("trajectory") as "trajectory")

    val spatioTemporalRangeVehicleDF = tempVehDF.select(
      $"trajectory_id",
      $"vehicle_id",
      $"trajectory.timestamp" as "timestamp",
      $"trajectory.location" as "location"
    )
    spatioTemporalRangeVehicleDF
  }

  def getKNNTrajectory(
      spark: SparkSession,
      dfTrajectory: DataFrame,
      trajectoryId: Long,
      neighbors: Int
  ): DataFrame = {
    dfTrajectory.createOrReplaceTempView("traj_data")
    val min_dist =
      "min(ST_Distance(ST_Point(a.trajectory.location[0],a.trajectory.location[1]),ST_Point(b.trajectory.location[0],b.trajectory.location[1])))";
    val outputUdf = spark.sql(
      "SELECT  b.trajectory_id FROM traj_data AS a, traj_data as b " +
        "WHERE a.trajectory_id=" + trajectoryId + " and b.trajectory_id!=" + trajectoryId + " GROUP BY b.trajectory_id ORDER BY " + min_dist + " limit " + neighbors
    );
    outputUdf
  }

}
