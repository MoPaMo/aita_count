// scripts.js

document.addEventListener("DOMContentLoaded", () => {
  const controller = new ScrollMagic.Controller();

  // Animate example messages
  document.querySelectorAll(".message").forEach((element, index) => {
    const tween = gsap
      .timeline()
      .fromTo(
        element,
        { opacity: 0, y: 50 },
        { opacity: 1, y: 0, duration: 0.5 }
      )
      .to(element, { opacity: 0, y: -50, delay: 0.5, duration: 0.5 });

    new ScrollMagic.Scene({
      triggerElement: ".messages",
      triggerHook: 0.5,
      duration: "100%", // Duration of the animation
      offset: index * window.innerHeight * 0.5, // Offset each message appearance
    })
      .setTween(tween)
      .addIndicators() // Add indicators (requires debug.addIndicators.js)
      .addTo(controller);
  });
});
