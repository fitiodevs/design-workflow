import 'package:flutter/animation.dart';

/// Tokens de curva de easing. Use sempre um destes em `curve:` de animations.
/// Nunca `Curves.ease*` built-in (genérico) nem `bounce`/`elastic` (amador).
///
/// Spec canônica: `docs/motion.md §3`. Persona: Jack (Coreógrafo).
abstract final class AppCurves {
  /// Entrada — punchy, responsivo. easeOutQuart.
  static const Curve enter = Cubic(0.23, 1.0, 0.32, 1.0);

  /// Saída — libera atenção rápido. easeInQuart.
  static const Curve exit = Cubic(0.76, 0.0, 0.86, 0.0);

  /// Movimento on-screen — suave. easeInOutCubic.
  static const Curve move = Cubic(0.65, 0.0, 0.35, 1.0);

  /// Loop sem aceleração.
  static const Curve linear = Curves.linear;

  /// Spring sutil — só pra celebrações Rive (não UI funcional). backOut suave.
  static const Curve celebrate = Cubic(0.34, 1.56, 0.64, 1.0);
}
