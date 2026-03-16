<script lang="ts">
  const thisYear = new Date().getFullYear();
  const visibleRadius = 4;
  const visibleCount = visibleRadius * 2 + 1;

  let {
    value = $bindable(thisYear + 1),
    minYear = thisYear + 1,
    maxYear,
    label = "Unlock year",
  }: {
    value?: number;
    minYear?: number;
    maxYear?: number | undefined;
    label?: string;
  } = $props();

  function clampYear(year: number) {
    const next = Math.max(minYear, Math.round(year));
    return typeof maxYear === "number" ? Math.min(maxYear, next) : next;
  }

  function step(delta: number) {
    value = clampYear(value + delta);
  }

  function selectYear(year: number) {
    value = clampYear(year);
  }

  function handleWheel(event: WheelEvent) {
    event.preventDefault();
    if (Math.abs(event.deltaY) < 4) return;
    step(event.deltaY > 0 ? 1 : -1);
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "ArrowUp") {
      event.preventDefault();
      step(-1);
    } else if (event.key === "ArrowDown") {
      event.preventDefault();
      step(1);
    } else if (event.key === "PageUp") {
      event.preventDefault();
      step(-10);
    } else if (event.key === "PageDown") {
      event.preventDefault();
      step(10);
    } else if (event.key === "Home") {
      event.preventDefault();
      value = minYear;
    } else if (event.key === "End" && typeof maxYear === "number") {
      event.preventDefault();
      value = maxYear;
    }
  }

  function getSlotStyle(offset: number) {
    const distance = Math.abs(offset);
    const angle = offset * 34;
    const radians = (angle * Math.PI) / 180;
    const x = Math.sin(radians) * 54;
    const y = offset * 46;
    const z = (Math.cos(radians) + 1) * -36;
    const rotateY = -angle;
    const scale = Math.max(0.68, 1 - distance * 0.08);
    const opacity = Math.max(0.2, 1 - distance * 0.17);

    return [
      `--slot-x:${x.toFixed(1)}px`,
      `--slot-y:${y.toFixed(1)}px`,
      `--slot-z:${z.toFixed(1)}px`,
      `--slot-rotate-y:${rotateY.toFixed(1)}deg`,
      `--slot-scale:${scale.toFixed(3)}`,
      `--slot-opacity:${opacity.toFixed(3)}`,
    ].join("; ");
  }

  $effect(() => {
    value = clampYear(Number(value) || minYear);
  });

  let slots = $derived.by(() => {
    const items = [];
    const startYear = Math.max(minYear, value - visibleRadius);

    for (let index = 0; index < visibleCount; index += 1) {
      const year = startYear + index;
      const offset = year - value;

      items.push({
        year,
        isSelected: year === value,
        tone: (year - minYear) % 2 === 0 ? "red" : "black",
        style: getSlotStyle(offset),
      });
    }

    return items;
  });
</script>

<div class="roulette">
  <div class="roulette__header">
    <span class="roulette__label">{label}</span>
    <span class="roulette__value mono">{value}</span>
  </div>

  <div
    class="roulette__wheel"
    role="spinbutton"
    tabindex="0"
    aria-label={label}
    aria-valuemin={minYear}
    aria-valuemax={typeof maxYear === "number" ? maxYear : undefined}
    aria-valuenow={value}
    onwheel={handleWheel}
    onkeydown={handleKeydown}
  >
    <button
      class="roulette__arrow roulette__arrow--up"
      type="button"
      aria-label="Previous year"
      onclick={() => step(-1)}
      disabled={value <= minYear}
    >
      ▲
    </button>

    <div class="roulette__track">
      <div class="roulette__shaft" aria-hidden="true"></div>
      <div class="roulette__focus" aria-hidden="true"></div>
      {#each slots as slot (`${slot.year}`)}
        <button
          class="roulette__slot"
          class:roulette__slot--selected={slot.isSelected}
          class:roulette__slot--red={slot.tone === "red"}
          class:roulette__slot--black={slot.tone === "black"}
          type="button"
          aria-pressed={slot.isSelected}
          style={slot.style}
          onclick={() => selectYear(slot.year)}
        >
          <span class="roulette__slot-ring"></span>
          <span class="roulette__slot-text mono">{slot.year}</span>
        </button>
      {/each}
    </div>

    <button
      class="roulette__arrow roulette__arrow--down"
      type="button"
      aria-label="Next year"
      onclick={() => step(1)}
      disabled={typeof maxYear === "number" && value >= maxYear}
    >
      ▼
    </button>
  </div>
</div>

<style lang="scss">
  @use "$lib/styles/variables" as *;

  $roulette-red: #a71919;
  $roulette-red-deep: #6e1010;
  $roulette-gold: #d6aa43;

  .roulette {
    width: min(100%, 24rem);
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
  }

  .roulette__header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
  }

  .roulette__label {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: $color-black-60;
  }

  .roulette__value {
    font-size: 1.75rem;
    line-height: 1;
    color: $color-black;
  }

  .roulette__wheel {
    @include glass(18px, rgba(255, 250, 244, 0.2), rgba(0, 0, 0, 0.12));
    position: relative;
    padding: 1rem 1rem 1.1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.85rem;
    background: radial-gradient(
        circle at 50% 0%,
        rgba(214, 170, 67, 0.24),
        transparent 44%
      ),
      linear-gradient(
        180deg,
        rgba(255, 255, 255, 0.34),
        rgba(255, 255, 255, 0.08)
      );
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.3),
      0 24px 40px rgba(0, 0, 0, 0.12);
    outline: none;

    &:focus-visible {
      box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.3),
        0 0 0 3px rgba(214, 170, 67, 0.45),
        0 24px 40px rgba(0, 0, 0, 0.12);
    }
  }

  .roulette__track {
    position: relative;
    width: 100%;
    height: 25rem;
    perspective: 1200px;
    perspective-origin: center;
    overflow: hidden;
    transform-style: preserve-3d;

    &::before,
    &::after {
      content: "";
      position: absolute;
      left: 0;
      right: 0;
      height: 4.4rem;
      z-index: 4;
      pointer-events: none;
    }

    &::before {
      top: 0;
      background: linear-gradient(
        180deg,
        rgba(250, 243, 232, 0.98),
        transparent
      );
    }

    &::after {
      bottom: 0;
      background: linear-gradient(0deg, rgba(250, 243, 232, 0.98), transparent);
    }
  }

  .roulette__shaft {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 2px;
    height: 100%;
    transform: translate(-50%, -50%);
    background: linear-gradient(
      180deg,
      transparent,
      rgba(214, 170, 67, 0.5),
      transparent
    );
    z-index: 0;
  }

  .roulette__focus {
    position: absolute;
    top: 50%;
    left: 50%;
    width: calc(100% - 0.8rem);
    height: 3.5rem;
    transform: translate(-50%, -50%);
    border: 2px solid rgba(214, 170, 67, 0.95);
    border-radius: 999px;
    box-shadow:
      inset 0 0 0 1px rgba(255, 255, 255, 0.34),
      0 0 24px rgba(214, 170, 67, 0.28);
    pointer-events: none;
    z-index: 5;
  }

  .roulette__slot {
    position: absolute;
    top: 50%;
    left: 50%;
    width: min(100%, 15rem);
    min-height: 3rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 0;
    border-radius: 999px;
    color: $color-white;
    cursor: pointer;
    transform-style: preserve-3d;
    transform: translate3d(
        calc(-50% + var(--slot-x)),
        calc(-50% + var(--slot-y)),
        var(--slot-z)
      )
      rotateY(var(--slot-rotate-y)) scale(var(--slot-scale));
    opacity: var(--slot-opacity);
    transition:
      transform $transition-fast,
      opacity $transition-fast,
      filter $transition-fast;
    filter: saturate(0.94);
    z-index: 1;
  }

  .roulette__slot-ring,
  .roulette__slot-text {
    position: relative;
    z-index: 1;
  }

  .roulette__slot-ring {
    position: absolute;
    inset: 0;
    border-radius: inherit;
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.15),
      inset 0 -10px 18px rgba(0, 0, 0, 0.16);
  }

  .roulette__slot--red {
    background: radial-gradient(
        circle at 28% 24%,
        rgba(255, 255, 255, 0.14),
        transparent 38%
      ),
      linear-gradient(180deg, $roulette-red, $roulette-red-deep);
  }

  .roulette__slot--black {
    background: radial-gradient(
        circle at 28% 24%,
        rgba(255, 255, 255, 0.1),
        transparent 38%
      ),
      linear-gradient(180deg, #202020, #050505);
  }

  .roulette__slot--selected {
    filter: saturate(1.06) brightness(1.05);
    z-index: 6;
  }

  .roulette__slot-text {
    font-size: 1.2rem;
    letter-spacing: 0.12em;
    text-shadow: 0 1px 0 rgba(0, 0, 0, 0.3);
  }

  .roulette__arrow {
    width: 2.5rem;
    height: 2.5rem;
    border: 0;
    border-radius: 999px;
    background: rgba(0, 0, 0, 0.82);
    color: $color-white;
    font-size: 0.85rem;
    cursor: pointer;
    transition:
      transform $transition-fast,
      background $transition-fast,
      opacity $transition-fast;

    &:hover:not(:disabled) {
      transform: scale(1.06);
      background: rgba(0, 0, 0, 0.94);
    }

    &:disabled {
      opacity: 0.35;
      cursor: default;
    }
  }

  @media (max-width: 640px) {
    .roulette {
      width: min(100%, 19rem);
    }

    .roulette__track {
      height: 22rem;
    }

    .roulette__slot {
      width: min(100%, 13rem);
    }

    .roulette__value {
      font-size: 1.5rem;
    }

    .roulette__slot-text {
      font-size: 1.05rem;
    }
  }
</style>
