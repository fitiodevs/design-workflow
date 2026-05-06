import 'package:flutter/material.dart';

/// Paleta semântica do Fitio — 29 tokens · NavyBlue/DarkBlue.
/// Acesso via `context.colors.<token>`.
///
/// Dois temas independentes (cada um tem valores fixos para um único modo):
///   - [navyBlue] — light exclusivo, seed #0817A1
///   - [darkBlue] — dark exclusivo, sem light variant
/// O MaterialApp.router conecta os dois ao sistema via `themeMode`.
class AppColors extends ThemeExtension<AppColors> {
  const AppColors({
    // Backgrounds
    required this.bgBase,
    required this.bgSurface,
    required this.bgSurfaceRaised,
    required this.bgInput,
    required this.bgSkeleton,
    required this.bgOverlay,
    // Brand / Ação
    required this.brandDefault,
    required this.brandMuted,
    required this.brandOnColor,
    required this.brandPressed,
    required this.brandDisabled,
    // Texto
    required this.textPrimary,
    required this.textSecondary,
    required this.textMuted,
    required this.textOnBrand,
    // Bordas
    required this.borderDefault,
    required this.borderStrong,
    required this.borderFocus,
    // Feedback semântico
    required this.feedbackSuccess,
    required this.feedbackSuccessMuted,
    required this.feedbackWarning,
    required this.feedbackWarningMuted,
    required this.feedbackError,
    required this.feedbackErrorMuted,
    required this.feedbackInfo,
    required this.feedbackInfoMuted,
    // Gamificação
    required this.gameAccent,
    required this.gameAccentMuted,
    required this.gameAccentOnColor,
  });

  // ── Backgrounds ────────────────────────────────────────────
  final Color bgBase;
  final Color bgSurface;
  final Color bgSurfaceRaised;
  final Color bgInput;
  final Color bgSkeleton;
  final Color bgOverlay;

  // ── Brand / Ação ───────────────────────────────────────────
  final Color brandDefault;
  final Color brandMuted;
  final Color brandOnColor;
  final Color brandPressed;
  final Color brandDisabled;

  // ── Texto ──────────────────────────────────────────────────
  final Color textPrimary;
  final Color textSecondary;
  final Color textMuted;
  final Color textOnBrand;

  // ── Bordas ─────────────────────────────────────────────────
  final Color borderDefault;
  final Color borderStrong;
  /// Sempre igual a brandDefault — nunca customizar separadamente.
  final Color borderFocus;

  // ── Feedback semântico ─────────────────────────────────────
  final Color feedbackSuccess;
  final Color feedbackSuccessMuted;
  final Color feedbackWarning;
  final Color feedbackWarningMuted;
  final Color feedbackError;
  final Color feedbackErrorMuted;
  final Color feedbackInfo;
  final Color feedbackInfoMuted;

  // ── Gamificação ────────────────────────────────────────────
  /// Âmbar para recompensa/destaque — distinto de feedbackWarning.
  /// Não precisa passar contraste de texto (uso decorativo/de destaque).
  final Color gameAccent;
  final Color gameAccentMuted;
  final Color gameAccentOnColor;

  // ── Mapa (pins / seleção navy) — valores fixos, ver [mapSelectionGlow]. ──
  /// Halo e traço neon do pin **selecionado** em mapas (Explorar, overlays).
  static const Color mapSelectionGlow = Color(0xFF00E5FF);
  /// Preenchimento disco do pin selecionado (contraste no glow).
  static const Color mapSelectionPin = Color(0xFF0A1F4D);
  /// Pin não selecionado (lista / camada Marker).
  static const Color mapMarkerDefault = Color(0xFF4A5578);

  // ── Instâncias de tema ─────────────────────────────────────

  /// Tema light exclusivo — seed #0817A1 · WCAG AA em todos os tokens de texto.
  static const AppColors navyBlue = AppColors(
    bgBase:          Color(0xFFF5F6FE),
    bgSurface:       Color(0xFFFFFFFF),
    bgSurfaceRaised: Color(0xFFFFFFFF),
    bgInput:         Color(0xFFFFFFFF),
    bgSkeleton:      Color(0xFFE8EAF6),
    bgOverlay:       Color(0x99000000),
    brandDefault:    Color(0xFF0817A1),
    brandMuted:      Color(0xFFD8DCFB),
    brandOnColor:    Color(0xFFFFFFFF),
    brandPressed:    Color(0xFF060F7A),
    brandDisabled:   Color(0xFFB0B8E8),
    textPrimary:     Color(0xFF0D0F1A),
    textSecondary:   Color(0xFF4A4E6B),
    textMuted:       Color(0xFF8B90B0),
    textOnBrand:     Color(0xFFFFFFFF),
    borderDefault:   Color(0xFFE8EAF6),
    borderStrong:    Color(0xFFC5CAE9),
    borderFocus:     Color(0xFF0817A1),
    feedbackSuccess:      Color(0xFF16A34A),
    feedbackSuccessMuted: Color(0xFFDCFCE7),
    feedbackWarning:      Color(0xFFD97706),
    feedbackWarningMuted: Color(0xFFFEF3C7),
    feedbackError:        Color(0xFFDC2626),
    feedbackErrorMuted:   Color(0xFFFEE2E2),
    feedbackInfo:         Color(0xFF1D4ED8),
    feedbackInfoMuted:    Color(0xFFDBEAFE),
    gameAccent:        Color(0xFFF59E0B),
    gameAccentMuted:   Color(0xFFFEF3C7),
    gameAccentOnColor: Color(0xFF78350F),
  );

  /// Tema dark exclusivo — par do NavyBlue no sistema operacional.
  static const AppColors darkBlue = AppColors(
    bgBase:          Color(0xFF121212),
    bgSurface:       Color(0xFF1E1E1E),
    bgSurfaceRaised: Color(0xFF1E1E1E),
    bgInput:         Color(0xFF1E1E1E),
    bgSkeleton:      Color(0xFF2C2C2E),
    bgOverlay:       Color(0x99000000),
    brandDefault:    Color(0xFF0817A1),
    brandMuted:      Color(0xFF1C2A6E),
    brandOnColor:    Color(0xFFFFFFFF),
    brandPressed:    Color(0xFF3A58FA),
    brandDisabled:   Color(0xFF2A3A6E),
    textPrimary:     Color(0xFFFFFFFF),
    textSecondary:   Color(0xFFB0B0B0),
    textMuted:       Color(0xFF8A8A8A),
    textOnBrand:     Color(0xFFFFFFFF),
    borderDefault:   Color(0xFF252D3D),
    borderStrong:    Color(0xFF2E3A50),
    borderFocus:     Color(0xFF4169E8),
    feedbackSuccess:      Color(0xFF4ADE80),
    feedbackSuccessMuted: Color(0xFF0D2E1A),
    feedbackWarning:      Color(0xFFFCD34D),
    feedbackWarningMuted: Color(0xFF2E1F00),
    feedbackError:        Color(0xFFFF5252),
    feedbackErrorMuted:   Color(0xFF2E0D0D),
    feedbackInfo:         Color(0xFF60A5FA),
    feedbackInfoMuted:    Color(0xFF0D1830),
    gameAccent:        Color(0xFFF59E0B),
    gameAccentMuted:   Color(0xFF2E1F00),
    gameAccentOnColor: Color(0xFFFCD34D),
  );

  @override
  AppColors copyWith({
    Color? bgBase,
    Color? bgSurface,
    Color? bgSurfaceRaised,
    Color? bgInput,
    Color? bgSkeleton,
    Color? bgOverlay,
    Color? brandDefault,
    Color? brandMuted,
    Color? brandOnColor,
    Color? brandPressed,
    Color? brandDisabled,
    Color? textPrimary,
    Color? textSecondary,
    Color? textMuted,
    Color? textOnBrand,
    Color? borderDefault,
    Color? borderStrong,
    Color? borderFocus,
    Color? feedbackSuccess,
    Color? feedbackSuccessMuted,
    Color? feedbackWarning,
    Color? feedbackWarningMuted,
    Color? feedbackError,
    Color? feedbackErrorMuted,
    Color? feedbackInfo,
    Color? feedbackInfoMuted,
    Color? gameAccent,
    Color? gameAccentMuted,
    Color? gameAccentOnColor,
  }) =>
      AppColors(
        bgBase:          bgBase          ?? this.bgBase,
        bgSurface:       bgSurface       ?? this.bgSurface,
        bgSurfaceRaised: bgSurfaceRaised ?? this.bgSurfaceRaised,
        bgInput:         bgInput         ?? this.bgInput,
        bgSkeleton:      bgSkeleton      ?? this.bgSkeleton,
        bgOverlay:       bgOverlay       ?? this.bgOverlay,
        brandDefault:    brandDefault    ?? this.brandDefault,
        brandMuted:      brandMuted      ?? this.brandMuted,
        brandOnColor:    brandOnColor    ?? this.brandOnColor,
        brandPressed:    brandPressed    ?? this.brandPressed,
        brandDisabled:   brandDisabled   ?? this.brandDisabled,
        textPrimary:     textPrimary     ?? this.textPrimary,
        textSecondary:   textSecondary   ?? this.textSecondary,
        textMuted:       textMuted       ?? this.textMuted,
        textOnBrand:     textOnBrand     ?? this.textOnBrand,
        borderDefault:   borderDefault   ?? this.borderDefault,
        borderStrong:    borderStrong    ?? this.borderStrong,
        borderFocus:     borderFocus     ?? this.borderFocus,
        feedbackSuccess:      feedbackSuccess      ?? this.feedbackSuccess,
        feedbackSuccessMuted: feedbackSuccessMuted ?? this.feedbackSuccessMuted,
        feedbackWarning:      feedbackWarning      ?? this.feedbackWarning,
        feedbackWarningMuted: feedbackWarningMuted ?? this.feedbackWarningMuted,
        feedbackError:        feedbackError        ?? this.feedbackError,
        feedbackErrorMuted:   feedbackErrorMuted   ?? this.feedbackErrorMuted,
        feedbackInfo:         feedbackInfo         ?? this.feedbackInfo,
        feedbackInfoMuted:    feedbackInfoMuted    ?? this.feedbackInfoMuted,
        gameAccent:        gameAccent        ?? this.gameAccent,
        gameAccentMuted:   gameAccentMuted   ?? this.gameAccentMuted,
        gameAccentOnColor: gameAccentOnColor ?? this.gameAccentOnColor,
      );

  @override
  AppColors lerp(ThemeExtension<AppColors>? other, double t) {
    if (other is! AppColors) return this;
    return AppColors(
      bgBase:          Color.lerp(bgBase,          other.bgBase,          t)!,
      bgSurface:       Color.lerp(bgSurface,       other.bgSurface,       t)!,
      bgSurfaceRaised: Color.lerp(bgSurfaceRaised, other.bgSurfaceRaised, t)!,
      bgInput:         Color.lerp(bgInput,         other.bgInput,         t)!,
      bgSkeleton:      Color.lerp(bgSkeleton,      other.bgSkeleton,      t)!,
      bgOverlay:       Color.lerp(bgOverlay,       other.bgOverlay,       t)!,
      brandDefault:    Color.lerp(brandDefault,    other.brandDefault,    t)!,
      brandMuted:      Color.lerp(brandMuted,      other.brandMuted,      t)!,
      brandOnColor:    Color.lerp(brandOnColor,    other.brandOnColor,    t)!,
      brandPressed:    Color.lerp(brandPressed,    other.brandPressed,    t)!,
      brandDisabled:   Color.lerp(brandDisabled,   other.brandDisabled,   t)!,
      textPrimary:     Color.lerp(textPrimary,     other.textPrimary,     t)!,
      textSecondary:   Color.lerp(textSecondary,   other.textSecondary,   t)!,
      textMuted:       Color.lerp(textMuted,       other.textMuted,       t)!,
      textOnBrand:     Color.lerp(textOnBrand,     other.textOnBrand,     t)!,
      borderDefault:   Color.lerp(borderDefault,   other.borderDefault,   t)!,
      borderStrong:    Color.lerp(borderStrong,    other.borderStrong,    t)!,
      borderFocus:     Color.lerp(borderFocus,     other.borderFocus,     t)!,
      feedbackSuccess:      Color.lerp(feedbackSuccess,      other.feedbackSuccess,      t)!,
      feedbackSuccessMuted: Color.lerp(feedbackSuccessMuted, other.feedbackSuccessMuted, t)!,
      feedbackWarning:      Color.lerp(feedbackWarning,      other.feedbackWarning,      t)!,
      feedbackWarningMuted: Color.lerp(feedbackWarningMuted, other.feedbackWarningMuted, t)!,
      feedbackError:        Color.lerp(feedbackError,        other.feedbackError,        t)!,
      feedbackErrorMuted:   Color.lerp(feedbackErrorMuted,   other.feedbackErrorMuted,   t)!,
      feedbackInfo:         Color.lerp(feedbackInfo,         other.feedbackInfo,         t)!,
      feedbackInfoMuted:    Color.lerp(feedbackInfoMuted,    other.feedbackInfoMuted,    t)!,
      gameAccent:        Color.lerp(gameAccent,        other.gameAccent,        t)!,
      gameAccentMuted:   Color.lerp(gameAccentMuted,   other.gameAccentMuted,   t)!,
      gameAccentOnColor: Color.lerp(gameAccentOnColor, other.gameAccentOnColor, t)!,
    );
  }
}

extension AppColorsContext on BuildContext {
  AppColors get colors => Theme.of(this).extension<AppColors>()!;
}


/// Cores de badge derivadas dos feedback tokens — fórmula:
///   bg     = feedbackXxxMuted
///   text   = feedbackXxx
///   border = feedbackXxx.withOpacity(0.3)
///
/// Acesso via `context.badgeColors.<status><Bg|Text|Border>`.
class AppBadgeColors extends ThemeExtension<AppBadgeColors> {
  const AppBadgeColors({
    required this.abertoBg,
    required this.abertoText,
    required this.abertoBorder,
    required this.rolandoBg,
    required this.rolandoText,
    required this.rolandoBorder,
    required this.encerradoBg,
    required this.encerradoText,
    required this.encerradoBorder,
    required this.ordemBg,
    required this.ordemText,
    required this.ordemBorder,
    required this.esgotadoBg,
    required this.esgotadoText,
    required this.esgotadoBorder,
    required this.finalizandoBg,
    required this.finalizandoText,
    required this.finalizandoBorder,
    required this.novoBg,
    required this.novoText,
    required this.novoBorder,
    required this.gratisBg,
    required this.gratisText,
    required this.gratisBorder,
  });

  final Color abertoBg;
  final Color abertoText;
  final Color abertoBorder;
  final Color rolandoBg;
  final Color rolandoText;
  final Color rolandoBorder;
  final Color encerradoBg;
  final Color encerradoText;
  final Color encerradoBorder;
  final Color ordemBg;
  final Color ordemText;
  final Color ordemBorder;
  final Color esgotadoBg;
  final Color esgotadoText;
  final Color esgotadoBorder;
  final Color finalizandoBg;
  final Color finalizandoText;
  final Color finalizandoBorder;
  final Color novoBg;
  final Color novoText;
  final Color novoBorder;
  final Color gratisBg;
  final Color gratisText;
  final Color gratisBorder;

  static AppBadgeColors fromAppColors(AppColors c) => AppBadgeColors(
        abertoBg:     c.feedbackSuccessMuted,
        abertoText:   c.feedbackSuccess,
        abertoBorder: c.feedbackSuccess.withValues(alpha: 0.3),
        rolandoBg:     c.feedbackSuccessMuted,
        rolandoText:   c.feedbackSuccess,
        rolandoBorder: c.feedbackSuccess.withValues(alpha: 0.3),
        encerradoBg:     c.bgSkeleton,
        encerradoText:   c.textSecondary,
        encerradoBorder: c.textSecondary.withValues(alpha: 0.3),
        ordemBg:     c.feedbackInfoMuted,
        ordemText:   c.feedbackInfo,
        ordemBorder: c.feedbackInfo.withValues(alpha: 0.3),
        esgotadoBg:     c.feedbackErrorMuted,
        esgotadoText:   c.feedbackError,
        esgotadoBorder: c.feedbackError.withValues(alpha: 0.3),
        finalizandoBg:     c.feedbackWarningMuted,
        finalizandoText:   c.feedbackWarning,
        finalizandoBorder: c.feedbackWarning.withValues(alpha: 0.3),
        novoBg:     c.feedbackInfoMuted,
        novoText:   c.feedbackInfo,
        novoBorder: c.feedbackInfo.withValues(alpha: 0.3),
        gratisBg:     c.feedbackSuccessMuted,
        gratisText:   c.feedbackSuccess,
        gratisBorder: c.feedbackSuccess.withValues(alpha: 0.3),
      );

  @override
  AppBadgeColors copyWith({
    Color? abertoBg, Color? abertoText, Color? abertoBorder,
    Color? rolandoBg, Color? rolandoText, Color? rolandoBorder,
    Color? encerradoBg, Color? encerradoText, Color? encerradoBorder,
    Color? ordemBg, Color? ordemText, Color? ordemBorder,
    Color? esgotadoBg, Color? esgotadoText, Color? esgotadoBorder,
    Color? finalizandoBg, Color? finalizandoText, Color? finalizandoBorder,
    Color? novoBg, Color? novoText, Color? novoBorder,
    Color? gratisBg, Color? gratisText, Color? gratisBorder,
  }) =>
      AppBadgeColors(
        abertoBg: abertoBg ?? this.abertoBg,
        abertoText: abertoText ?? this.abertoText,
        abertoBorder: abertoBorder ?? this.abertoBorder,
        rolandoBg: rolandoBg ?? this.rolandoBg,
        rolandoText: rolandoText ?? this.rolandoText,
        rolandoBorder: rolandoBorder ?? this.rolandoBorder,
        encerradoBg: encerradoBg ?? this.encerradoBg,
        encerradoText: encerradoText ?? this.encerradoText,
        encerradoBorder: encerradoBorder ?? this.encerradoBorder,
        ordemBg: ordemBg ?? this.ordemBg,
        ordemText: ordemText ?? this.ordemText,
        ordemBorder: ordemBorder ?? this.ordemBorder,
        esgotadoBg: esgotadoBg ?? this.esgotadoBg,
        esgotadoText: esgotadoText ?? this.esgotadoText,
        esgotadoBorder: esgotadoBorder ?? this.esgotadoBorder,
        finalizandoBg: finalizandoBg ?? this.finalizandoBg,
        finalizandoText: finalizandoText ?? this.finalizandoText,
        finalizandoBorder: finalizandoBorder ?? this.finalizandoBorder,
        novoBg: novoBg ?? this.novoBg,
        novoText: novoText ?? this.novoText,
        novoBorder: novoBorder ?? this.novoBorder,
        gratisBg: gratisBg ?? this.gratisBg,
        gratisText: gratisText ?? this.gratisText,
        gratisBorder: gratisBorder ?? this.gratisBorder,
      );

  @override
  AppBadgeColors lerp(ThemeExtension<AppBadgeColors>? other, double t) {
    if (other is! AppBadgeColors) return this;
    return AppBadgeColors(
      abertoBg:     Color.lerp(abertoBg,     other.abertoBg,     t)!,
      abertoText:   Color.lerp(abertoText,   other.abertoText,   t)!,
      abertoBorder: Color.lerp(abertoBorder, other.abertoBorder, t)!,
      rolandoBg:     Color.lerp(rolandoBg,     other.rolandoBg,     t)!,
      rolandoText:   Color.lerp(rolandoText,   other.rolandoText,   t)!,
      rolandoBorder: Color.lerp(rolandoBorder, other.rolandoBorder, t)!,
      encerradoBg:     Color.lerp(encerradoBg,     other.encerradoBg,     t)!,
      encerradoText:   Color.lerp(encerradoText,   other.encerradoText,   t)!,
      encerradoBorder: Color.lerp(encerradoBorder, other.encerradoBorder, t)!,
      ordemBg:     Color.lerp(ordemBg,     other.ordemBg,     t)!,
      ordemText:   Color.lerp(ordemText,   other.ordemText,   t)!,
      ordemBorder: Color.lerp(ordemBorder, other.ordemBorder, t)!,
      esgotadoBg:     Color.lerp(esgotadoBg,     other.esgotadoBg,     t)!,
      esgotadoText:   Color.lerp(esgotadoText,   other.esgotadoText,   t)!,
      esgotadoBorder: Color.lerp(esgotadoBorder, other.esgotadoBorder, t)!,
      finalizandoBg:     Color.lerp(finalizandoBg,     other.finalizandoBg,     t)!,
      finalizandoText:   Color.lerp(finalizandoText,   other.finalizandoText,   t)!,
      finalizandoBorder: Color.lerp(finalizandoBorder, other.finalizandoBorder, t)!,
      novoBg:     Color.lerp(novoBg,     other.novoBg,     t)!,
      novoText:   Color.lerp(novoText,   other.novoText,   t)!,
      novoBorder: Color.lerp(novoBorder, other.novoBorder, t)!,
      gratisBg:     Color.lerp(gratisBg,     other.gratisBg,     t)!,
      gratisText:   Color.lerp(gratisText,   other.gratisText,   t)!,
      gratisBorder: Color.lerp(gratisBorder, other.gratisBorder, t)!,
    );
  }
}

extension AppBadgeColorsContext on BuildContext {
  AppBadgeColors get badgeColors => Theme.of(this).extension<AppBadgeColors>()!;
}
