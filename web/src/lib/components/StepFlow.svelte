<script lang="ts">
  import { onMount } from "svelte";
  import type { Snippet } from "svelte";

  let {
    steps,
    current = $bindable(0),
    fullscreen = false,
  }: {
    steps: Snippet[];
    current?: number;
    fullscreen?: boolean;
  } = $props();

  let container = $state<HTMLDivElement | null>(null);
  let syncedIndex = $state(0);
  let sectionNodes: HTMLElement[] = [];

  function clampIndex(index: number) {
    return Math.max(0, Math.min(index, steps.length - 1));
  }

  function scrollToIndex(index: number, behavior: ScrollBehavior = "smooth") {
    const next = clampIndex(index);
    syncedIndex = next;

    if (fullscreen) {
      if (!container) return;

      container.scrollTo({
        top: next * container.clientHeight,
        behavior,
      });
      return;
    }

    sectionNodes[next]?.scrollIntoView({
      behavior,
      block: "start",
    });
  }

  function go(dir: number) {
    current = clampIndex(current + dir);
  }

  function registerSection(node: HTMLElement, index: number) {
    sectionNodes[index] = node;

    return {
      destroy() {
        sectionNodes[index] = undefined as unknown as HTMLElement;
      },
    };
  }

  function onKeydown(e: KeyboardEvent) {
    if (
      e.target instanceof HTMLElement &&
      e.target.closest("input, textarea, button, select, [contenteditable='true']")
    ) {
      return;
    }

    if (e.key === "ArrowDown" || e.key === "Enter") {
      e.preventDefault();
      go(1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      go(-1);
    }
  }

  function onScroll() {
    if (!fullscreen || !container) return;

    const next = clampIndex(
      Math.round(container.scrollTop / container.clientHeight),
    );

    syncedIndex = next;

    if (next !== current) {
      current = next;
    }
  }

  $effect(() => {
    const next = clampIndex(current);

    if (next !== syncedIndex) {
      scrollToIndex(next);
    }
  });

  onMount(() => {
    scrollToIndex(current, "auto");

    let observer: IntersectionObserver | undefined;

    if (!fullscreen) {
      observer = new IntersectionObserver(
        (entries) => {
          const visibleEntry = entries
            .filter((entry) => entry.isIntersecting)
            .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

          if (!visibleEntry) return;

          const next = sectionNodes.findIndex((node) => node === visibleEntry.target);
          if (next === -1) return;

          syncedIndex = next;

          if (next !== current) {
            current = next;
          }
        },
        {
          threshold: [0.35, 0.6],
        },
      );

      for (const node of sectionNodes) {
        if (node) observer.observe(node);
      }
    }

    function onResize() {
      if (fullscreen) {
        scrollToIndex(current, "auto");
      }
    }

    window.addEventListener("resize", onResize);

    return () => {
      observer?.disconnect();
      window.removeEventListener("resize", onResize);
    };
  });
</script>

<svelte:window onkeydown={onKeydown} />

<div
  class="step-flow"
  class:step-flow--fullscreen={fullscreen}
  class:step-flow--page={!fullscreen}
  bind:this={container}
  onscroll={fullscreen ? onScroll : undefined}
>
  {#each steps as step, i}
    <section
      class="step"
      class:step--fullscreen={fullscreen}
      class:step--page={!fullscreen}
      class:active={i === current}
      use:registerSection={i}
    >
      {@render step()}
    </section>
  {/each}

  <nav class="step-nav" aria-label="Step navigation">
    <button
      class="step-nav__btn"
      onclick={() => go(-1)}
      disabled={current === 0}
      aria-label="Previous step"
    >
      &#9650;
    </button>
    <span class="step-nav__count">{current + 1}/{steps.length}</span>
    <button
      class="step-nav__btn"
      onclick={() => go(1)}
      disabled={current === steps.length - 1}
      aria-label="Next step"
    >
      &#9660;
    </button>
  </nav>
</div>

<style lang="scss">
  @use "$lib/styles/variables" as *;

  .step-flow {
    position: relative;
  }

  .step {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .step-flow--fullscreen {
    position: fixed;
    inset: 0;
    overflow-y: scroll;
    overscroll-behavior-y: contain;
    scroll-behavior: smooth;
    scroll-snap-type: y mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: auto;
    scrollbar-color: $color-black $color-white-20;
  }

  .step--fullscreen {
    min-height: 100svh;
    padding: 2rem;
    scroll-snap-align: start;
    scroll-snap-stop: always;
  }

  .step-flow--page {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 6rem 1.5rem 3rem;
  }

  .step--page {
    min-height: auto;
    padding: 0;
  }

  .step-flow--fullscreen::-webkit-scrollbar {
    width: 14px;
  }

  .step-flow--fullscreen::-webkit-scrollbar-track {
    background: $color-white-20;
  }

  .step-flow--fullscreen::-webkit-scrollbar-thumb {
    background: $color-black;
    border: 3px solid $color-white-20;
    border-radius: 999px;
  }

  .step-nav {
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    z-index: 10;
  }

  .step-nav__btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    color: $color-white;
    background: $color-black-50;
    border: 1px solid $color-white-20;
    border-radius: 50%;
    cursor: pointer;
    transition: background $transition-fast;

    &:hover:not(:disabled) {
      background: $color-black-80;
    }

    &:disabled {
      opacity: 0.3;
      cursor: default;
    }
  }

  .step-nav__count {
    font-size: 0.75rem;
    color: $color-black-60;
    font-family: $font-mono;
  }
</style>
