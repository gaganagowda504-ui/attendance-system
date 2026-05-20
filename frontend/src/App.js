function App() {

  const attendanceData = [
    {
      name: "Gagana",
      date: "19-05-2026",
      time: "10:00 AM"
    },
    {
      name: "Rahul",
      date: "19-05-2026",
      time: "10:05 AM"
    }
  ];

  return (
    <div style={{ padding: "20px" }}>
      <h1>Attendance System</h1>

      <table
        border="1"
        cellPadding="12"
        style={{
          borderCollapse: "collapse",
          fontSize: "24px"
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
    </div>
  );
}

export default App;