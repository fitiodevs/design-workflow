/// Tokens de duração de motion. Use sempre um destes valores em
/// `Duration(...)` de animations. Nunca hard-code `200ms`, `300ms` etc.
///
/// Spec canônica: `docs/motion.md`. Persona: Jack (Coreógrafo).
abstract final class AppMotion {
  static const Duration instant     = Duration(milliseconds: 80);
  static const Duration fast        = Duration(milliseconds: 150);
  static const Duration normal      = Duration(milliseconds: 220);
  static const Duration slow        = Duration(milliseconds: 300);
  static const Duration route       = Duration(milliseconds: 320);
  static const Duration celebration = Duration(milliseconds: 1200);

  static const Duration shimmer = Duration(milliseconds: 2400);
  static const Duration pulse   = Duration(milliseconds: 1800);

  static const Duration staggerShort = Duration(milliseconds: 40);
  static const Duration staggerLong  = Duration(milliseconds: 80);
}
