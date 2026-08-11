import { useState, useEffect } from "react";
import api from "./api";

function CheckInHistory() {
  const [checkinArray, setCheckinArray] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    async function getAPICheckins() {
      // TODO: check this path against how api.js's baseURL is configured —
      // baseURL already ends in "/api/". Compare against how CheckInForm.jsx
      // calls api.post("checkins/", ...) — is "api/checkins/" here going to
      // build the same URL, or a different one? Check the Network tab request
      // URL once you run this to be sure.
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

      // TODO: this request can fail (401 with no/expired token, network error,
      // 500, etc.) just like the POST in CheckInForm.jsx can. Right now a
      // failure here throws inside this async function with nothing catching
      // it. Wrap the await above in a try/catch, same shape as handleSubmit.

      // TODO: the response comes back but nothing is done with it — call
      // setCheckinArray with the data from the response so it actually lands
      // in state. (On the error path, you'll want setErrorMessage too.)
    }

    getAPICheckins();

    // TODO: "return ()" isn't valid JS on its own — a useEffect callback must
    // either return nothing at all, or return a cleanup function (an actual
    // function, e.g. `return () => { ... }`, not empty parens with nothing after).
    // Ask yourself: does this effect have anything to clean up? (Hint: think about
    // what "cleanup" means for a fetch — e.g. what if the component unmounts before
    // the request finishes.) If you don't have an answer yet, it's fine to just
    // delete this line for a first working version and revisit later.
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

  // TODO: nothing is returned from the component itself yet, so nothing will
  // render. Add a `return (...)` here with actual JSX: loop over checkinArray
  // with .map() and render something per check-in (date, sleep hours, soreness
  // level, energy level, notes). Also decide what to show while checkinArray is
  // still empty (loading?) and what to show if errorMessage is set.
}

export default CheckInHistory;
