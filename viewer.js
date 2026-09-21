const viewer = document.querySelector("#grasp-viewer");
const tabs = Array.from(document.querySelectorAll(".viewer-tab"));

if (viewer && tabs.length > 0) {
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      if (tab.getAttribute("aria-selected") === "true") return;

      tabs.forEach((otherTab) => {
        const isSelected = otherTab === tab;
        otherTab.classList.toggle("is-active", isSelected);
        otherTab.setAttribute("aria-selected", String(isSelected));
      });

      viewer.setAttribute("aria-labelledby", tab.id);
      viewer.title = `Interactive QUAD Hand ${tab.textContent.trim().toLowerCase()} grasp`;
      const playbackPath = encodeURIComponent(tab.dataset.viewerSrc);
      viewer.src = `./viser/client/?playbackPath=${playbackPath}`;
    });
  });
}
