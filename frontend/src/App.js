import { CSVLink } from "react-csv";
import "./App.css";
import Webcam from "react-webcam";
import { useRef, useState } from "react";
import axios from "axios";

function App() {

  const webcamRef = useRef(null);

  const [name, setName] = useState("");

  const [attendanceData, setAttendanceData] = useState(
    JSON.parse(localStorage.getItem("attendance")) || []
  );

  const capture = async () => {

    const imageSrc = webcamRef.current.getScreenshot();

    const response = await axios.post(
      "http://127.0.0.1:5000/upload",
      {
        image: imageSrc,
        name: name
      }
    );

    const currentDate = new Date().toLocaleDateString();

   const currentTime = new Date().toLocaleTimeString([], {
  hour: '2-digit',
  minute: '2-digit'
});

    if (response.data.message.includes("Attendance Marked")) {

      const newAttendance = {
        name: name,
        date: currentDate,
        time: currentTime
      };

      const updatedAttendance = [
        ...attendanceData,
        newAttendance
      ];

      setAttendanceData(updatedAttendance);

      localStorage.setItem(
        "attendance",
        JSON.stringify(updatedAttendance)
      );
    }

    alert(response.data.message);

    setName("");
  };

  return (
    <div className="container">

      <h1>Attendance Monitoring System</h1>

      {/* INPUT */}
      <input
        type="text"
        placeholder="Enter Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={{
          padding: "10px",
          fontSize: "18px"
        }}
      />

      <br /><br />

      {/* WEBCAM */}
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={400}
      />

      <br /><br />

      {/* BUTTON */}
      <button
        className="button"
        onClick={capture}
        style={{
          padding: "10px",
          fontSize: "18px"
        }}
      >
        Mark Attendance
      </button>

      <br /><br />

      {/* TABLE */}
      <table
        className="table"
        border="1"
        cellPadding="10"
        style={{
          borderCollapse: "collapse",
          fontSize: "18px"
        }}
      >
        <thead>
          <tr>
            <th>Name</th>
            <th>Date</th>
            <th>Time</th>
          </tr>
        </thead>

        <tbody>
          {attendanceData.map((item, index) => (
            <tr key={index}>
              <td>{item.name}</td>
              <td>{item.date}</td>
              <td>{item.time}</td>
            </tr>
          ))}
        </tbody>

      </table>

      <br />

      {/* DOWNLOAD CSV */}
      <CSVLink
        data={attendanceData}
        filename={"attendance.csv"}
      >

        <button className="button">
          Download Attendance CSV
        </button>

      </CSVLink>

    </div>
  );
}

export default App;