const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const withRetry = ({
  task,
  onDone,
  onRetry,
  onGiveUp,
  nRetry,
  waitMillis,
}) => async (args) => {
  while (nRetry > 0) {
    try {
      const result = await task(args);
      if (result) {
        return (onDone && onDone(result)) || result;
      }
      onRetry && onRetry(null);
    } catch (e) {
      onRetry && onRetry(e);
    }
    --nRetry;
    await sleep(waitMillis);
  }
  return onGiveUp && onGiveUp();
};
const fetchOrNull = async (url, opts) => {
  const response = await fetch(url, opts);
  if (response.ok) {
    return await response.text();
  }
  return null;
};
const paintVisits = (value) =>
  (document.querySelector("#visits").innerText = value);
const paintGiveUp = () =>
  (document.querySelector("#visits").innerText = "I give up :( ");
const paintRetry = () =>
  (document.querySelector("#visits").innerText = "Retrying... :| ");

const SERVICE_URL = "/api/visits"; // "/site/api/visits";
const getVisits = withRetry({
  task: (pageName) => fetchOrNull(SERVICE_URL + `/${pageName}`),
  onDone: paintVisits,
  onGiveUp: paintGiveUp,
  onRetry: paintRetry,
  nRetry: 1,
  waitMillis: 1000,
});

const logPost = (msg) => (obj) => console.log(msg, obj);
const postVisit = withRetry({
  task: (pageName) =>
    fetchOrNull(SERVICE_URL + `/${pageName}`, {
      method: "POST",
    }),
  onDone: logPost("Post done"),
  onGiveUp: logPost("Post given up"),
  onRetry: logPost("Post retry"),
  nRetry: 1,
  waitMillis: 1000,
});
