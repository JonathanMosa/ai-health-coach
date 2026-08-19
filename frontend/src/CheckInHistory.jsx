import { useState, useEffect } from "react";
import api from "./api";

function CheckInHistory() {
  const [checkinArray, setCheckinArray] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function getAPICheckins() {
      try {
        const response = await api.get("checkins/");
        setCheckinArray(response.data);
      } catch (error) {
        const data = error.response?.data;
        const message = data
          ? Object.values(data).flat().join(" ")
          : "Something went wrong. Please try again.";
        setErrorMessage(message);
      }
    }

    getAPICheckins();

    return () => {};
  }, []);

  return (
    <>
      <ul>
        {checkinArray.map((checkin) => (
          <li key={checkin.date}>
            {checkin.date}: slept {checkin.sleep_hours}h, soreness{" "}
            {checkin.soreness_level}, energy {checkin.energy_level} —{" "}
            {checkin.notes}
          </li>
        ))}
      </ul>
      <p style={{ color: "red" }}>{errorMessage}</p>
    </>
  );
}

export default CheckInHistory;
