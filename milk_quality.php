<!DOCTYPE html>
<html>
<head>
 <title>Milk Quality</title>
<style>
  table {
   border-collapse: collapse;
   width: 100%;
   color: #000000;
   font-family: monospace;
   font-size: 18px;
   text-align: center;
     } 
  th {
   background-color: #7ACDF7;
   color: white;
    }
  tr:nth-child(even) {background-color: #f2f2f2}
 </style>
</head>
<body>
 <table>
 <tr>
  <th>Time</th>
  <th>Milk Man ID</th> 
  <th>pH Reading</th> 
  <th>Colour Grade</th>
  <th>Temperature</th>
  <th>LR</th>
  <th>CLR</th>
  <th>Total Grade</th>
 </tr>
 <?php
$conn = mysqli_connect("localhost", "root", "", "quality_inf");
  // Check connection
  if ($conn->connect_error) {
   die("Connection failed: " . $conn->connect_error);
  } 
  $sql = "SELECT Time,Milk_Man_ID,pH_Reading,Colour_Grade,Temperature,LR,CLR,Total_Grade FROM milk_quality";
  $result = $conn->query($sql);
  if ($result->num_rows > 0) {
   // output data of each row
   while($row = $result->fetch_assoc()) {
    echo "<tr> <td>" . $row["Time"] . "</td> <td>" . $row["Milk_Man_ID"] . "</td> <td>" . $row["pH_Reading"] ."</td> <td>" . $row["Colour_Grade"] ."</td> <td>" . $row["Temperature"] . "</td> <td>" . $row["LR"] . "</td> <td>" . $row["CLR"] . "</td> <td>". $row["Total_Grade"] . "</td></tr>";
}
echo "</table>";
} else { echo "0 results"; }
$conn->close();
?>
</table>
</body>
</html>