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

  // ✅ IMPORTANT: PUT YOUR REAL RENDER LINK HERE
  const API = "https://YOUR-BACKEND-RENDER-URL.onrender.com";

  const capture = async () => {
    try {
      if (!name) {
        alert("Please enter name");
        return;
      }

      const imageSrc = webcamRef.current?.getScreenshot();

      if (!imageSrc) {
        alert("Camera not ready. Allow permission.");
        return;
      }

      console.log("Sending request to backend...");

      const response = await axios.post(
        `${API}/upload`,
        {
          image: imageSrc,
          name: name,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const currentDate = new Date().toLocaleDateString();

      const currentTime = new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });

      if (response.data.message.includes("Attendance Marked")) {
        const newAttendance = {
          name: name,
          date: currentDate,
          time: currentTime,
        };

        const updated = [...attendanceData, newAttendance];

        setAttendanceData(updated);
        localStorage.setItem("attendance", JSON.stringify(updated));
      }

      alert(response.data.message);
      setName("");
    } catch (error) {
      console.log("Backend Error:", error.message);
      alert("Backend not reachable. Check Render URL or server.");
    }
  };

  return (
    <div className="container">
      <h1>Attendance Monitoring System</h1>

      <input
        type="text"
        placeholder="Enter Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={{ padding: "10px", fontSize: "18px" }}
      />

      <br />
      <br />

      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={400}
      />

      <br />
      <br />

      <button className="button" onClick={capture} type="button">
        Mark Attendance
      </button>

      <br />
      <br />

      <table border="1" cellPadding="10">
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

      <CSVLink data={attendanceData} filename={"attendance.csv"}>
        <button className="button">Download CSV</button>
      </CSVLink>
    </div>
  );
}

export default App;