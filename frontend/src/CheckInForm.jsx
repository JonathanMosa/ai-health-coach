import { useState } from "react";
import api from "./api";

function CheckInForm() {
  const [sleepHours, setSleepHours] = useState("");
  const [sorenessLevel, setSorenessLevel] = useState("");
  const [energyLevel, setEnergyLevel] = useState("");
  const [notes, setNotes] = useState("");
  const [status, setStatus] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus("submitting");

    // TODO: call api.post("checkins/", { ... }) with the four fields above
    try {
      await api.post("checkins/", {
        sleep_hours: sleepHours,
        soreness_level: sorenessLevel,
        energy_level: energyLevel,
        notes,
      });
      // success path
      setStatus("success");

      setSleepHours("");
      setSorenessLevel("");
      setEnergyLevel("");
      setNotes("");
    } catch (error) {
      // failure path
      const data = error.response?.data;
      const message = data
        ? Object.values(data).flat().join(" ")
        : "Something went wrong. Please try again.";

      setStatus("error");
      setErrorMessage(message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Sleep hours
        <input
          type="number"
          value={sleepHours}
          onChange={(e) => setSleepHours(e.target.value)}
        />
      </label>

      <label>
        Soreness level (1-5)
        <input
          type="number"
          value={sorenessLevel}
          onChange={(e) => setSorenessLevel(e.target.value)}
        />
      </label>

      <label>
        Energy level (1-5)
        <input
          type="number"
          value={energyLevel}
          onChange={(e) => setEnergyLevel(e.target.value)}
        />
      </label>

      <label>
        Notes
        <textarea value={notes} onChange={(e) => setNotes(e.target.value)} />
      </label>

      <button type="submit">Submit</button>

      {status === "submitting" && <p>Saving...</p>}
      {status === "success" && <p>Check-in saved.</p>}
      {status === "error" && <p style={{ color: "red" }}>{errorMessage}</p>}
    </form>
  );
}

export default CheckInForm;
