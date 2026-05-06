import 'package:flutter/material.dart';

import '../../gen/fonts.gen.dart';
import 'font_scale.dart';

/// Tipografia baseada nas fontes Plus Jakarta Sans (títulos) + MSJH (corpo).
///
/// O [scale] aplica multiplicador no tamanho e incremento de peso em todos os
/// estilos do `TextTheme`, permitindo A / A+ / A++.
TextTheme buildAppTextTheme({
  required Color bodyColor,
  required Color displayColor,
  FontScale scale = FontScale.a,
}) {
  final sizeK = scale.sizeMultiplier;
  final wSteps = scale.weightSteps;

  TextStyle title(double fontSize, {double height = 1.25, FontWeight w = FontWeight.w700}) =>
      TextStyle(
        fontFamily: FontFamily.plusJakartaSans,
        fontWeight: bumpFontWeight(w, wSteps),
        fontSize: fontSize * sizeK,
        height: height,
        color: displayColor,
      );

  TextStyle body(double fontSize, {double height = 1.4, FontWeight w = FontWeight.w500}) =>
      TextStyle(
        fontFamily: FontFamily.msjh,
        fontWeight: bumpFontWeight(w, wSteps),
        fontSize: fontSize * sizeK,
        height: height,
        color: bodyColor,
      );

  return TextTheme(
    displaySmall: title(36, height: 1.22),
    headlineMedium: title(28, height: 1.28),
    headlineSmall: title(24, height: 1.33),
    titleLarge: title(22),
    titleMedium: title(18),
    titleSmall: title(16),
    bodyLarge: body(16),
    bodyMedium: body(14),
    bodySmall: body(12),
    labelLarge: body(14, height: 1.43),
    labelMedium: body(12, height: 1.33),
    labelSmall: body(11, height: 1.45),
  );
}
