import { Body, Controller, Get, Post, Query, UseGuards } from '@nestjs/common'
import {
  ApiBearerAuth,
  ApiBody,
  ApiConsumes,
  ApiOperation,
  ApiTags,
} from '@nestjs/swagger'
import { JwtAuthGuard } from '../auth/jwt/jwt-auth.guard'
import { CommentRegisterInputDto } from './dtos/comment.register.dto'
import { User } from '../common/decorators/user.decorator'
import { UserEntity } from '../auth/entities/user.entity'
import { CommentService } from './comment.service'
import { CommentsGetInputDto } from './dtos/comments.get.dto'
import { CommentsMyInputDto } from './dtos/comments.my.dto'

@Controller('comment')
@ApiTags('comment')
export class CommentController {
  constructor(private readonly commentService: CommentService) {}

  @UseGuards(JwtAuthGuard)
  @Post()
  @ApiConsumes('application/x-www-form-urlencoded')
  @ApiBearerAuth('access-token')
  @ApiBody({ type: CommentRegisterInputDto })
  async register(
    @Body() commentRegisterInputDto: CommentRegisterInputDto,
    @User() user: UserEntity,
  ) {
    return await this.commentService.register(user, commentRegisterInputDto)
  }

  @Get()
  @ApiOperation({
    summary: 'Get comments',
  })
  async getAll(@Query() commentsGetInputDto: CommentsGetInputDto) {
    return await this.commentService.getAll(commentsGetInputDto)
  }

  @UseGuards(JwtAuthGuard)
  @ApiBearerAuth('access-token')
  @Get('my')
  @ApiOperation({ summary: 'Get my comments' })
  async getMy(
    @Query() commentsMyInputDto: CommentsMyInputDto,
    @User() user: UserEntity,
  ) {
    return await this.commentService.getMy(user, commentsMyInputDto)
  }
}
