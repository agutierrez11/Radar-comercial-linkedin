export function cx(...classes: readonly (string | undefined | false)[]): string {
  return classes.filter(Boolean).join(" ")
}
