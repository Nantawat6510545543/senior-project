// // Unused for now
function PlotImage({ type }) {
  if (!type) return null;

  const src = `http://localhost:8000/plot?type=${type}&t=${Date.now()}`;
  return <img src={src} alt={type} />;
}

export default PlotImage