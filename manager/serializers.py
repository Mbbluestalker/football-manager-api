from rest_framework import serializers

from .lib.utils import Util
from .models import Player, Team, User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "team_name",
            "profile_image",
            "password",
        ]

        # Prevents the password from showing after submission
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        new_user = User.objects.create(**validated_data)
        new_user.set_password(validated_data["password"])
        team = Team.objects.create(
            name=validated_data["team_name"],
            user=new_user,
            country=Util.get_country(),
        )

        for player in range(0, 20):
            name = Util.generate_player_name()

            # create 3 goal keepers
            if player in range(0, 3):
                generated_player = Player.objects.create(
                    first_name=name[0],
                    last_name=name[1],
                    age=Util.generate_age(),
                    team=team,
                    position="Goal_Keeper",
                    shirt_number=player + 1,
                    country=Util.get_country(),
                )

            # create 6 defenders
            if player in range(3, 9):
                generated_player = Player.objects.create(
                    first_name=name[0],
                    last_name=name[1],
                    age=Util.generate_age(),
                    team=team,
                    position="Defender",
                    shirt_number=player + 1,
                    country=Util.get_country(),
                )

            # create 6 Midfielders
            if player in range(9, 15):
                generated_player = Player.objects.create(
                    first_name=name[0],
                    last_name=name[1],
                    age=Util.generate_age(),
                    team=team,
                    position="Midfielder",
                    shirt_number=player + 1,
                    country=Util.get_country(),
                )

            # create 5 Attackers
            if player in range(15, 20):
                generated_player = Player.objects.create(
                    first_name=name[0],
                    last_name=name[1],
                    age=Util.generate_age(),
                    team=team,
                    position="Attackers",
                    shirt_number=player + 1,
                    country=Util.get_country(),
                )

            generated_player.save()
        new_user.save()
        return new_user
    
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()