function openImage(image_url) {
  window.open(image_url, '_blank');
}

function deleteReport(assetId) {
  fetch("/deletereport", {
    method: "POST",
    body: JSON.stringify({ asset_id: assetId }),
  }).then((_res) => {
    window.location.href = "/reports";
  });
}

function approveReport(assetId) {
  fetch("/approvereport", {
    method: "POST",
    body: JSON.stringify({ asset_id: assetId }),
  }).then((_res) => {
    window.location.href = "/reports";
  });
}