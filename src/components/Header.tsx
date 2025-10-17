import { Bell, Settings, Trophy, GraduationCap, TrendingUp, User } from "lucide-react";
import { Button } from "./ui/button";

interface HeaderProps {
  onArcadeClick: () => void;
  onLeaderboardClick: () => void;
  onNotificationClick: () => void;
  onProfileClick: () => void;
}

export const Header = ({ onArcadeClick, onLeaderboardClick, onNotificationClick, onProfileClick }: HeaderProps) => {
  return (
    <header className="glass-panel p-4 mb-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-heading text-3xl font-bold gradient-text">
            StockVerse
          </h1>
          <p className="text-sm text-muted-foreground">Play. Learn. Invest.</p>
        </div>
        
        <div className="flex items-center gap-4">
          <Button 
            onClick={onArcadeClick}
            className="glass-panel-bright hover:scale-105 transition-transform text-white flex items-center gap-2"
            data-tour="arcade"
          >
            <GraduationCap className="w-4 h-4" />
            <TrendingUp className="w-4 h-4" />
            <span className="hidden sm:inline">Arcade</span>
          </Button>
          
          <Button 
            variant="ghost" 
            size="icon" 
            className="relative" 
            data-tour="notifications"
            onClick={onNotificationClick}
          >
            <Bell className="w-5 h-5" />
            <span className="absolute top-0 right-0 w-2 h-2 bg-destructive rounded-full animate-pulse" />
          </Button>
          
          <Button variant="ghost" size="icon" data-tour="trophy" onClick={onLeaderboardClick}>
            <Trophy className="w-5 h-5" />
          </Button>
          
          <Button 
            variant="ghost" 
            size="icon" 
            data-tour="settings"
            onClick={onProfileClick}
            title="Customize Profile"
          >
            <User className="w-5 h-5" />
          </Button>
        </div>
      </div>
    </header>
  );
};
